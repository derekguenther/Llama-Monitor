"""Electricity cost calculator for llama-monitor."""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from database import Database


class ElectricityCostCalculator:
    """Calculates electricity cost based on power consumption."""

    def __init__(
        self,
        database: Database,
        idle_baseline_w: float = 150.0,  # Default idle power
    ):
        """Initialize the calculator.

        Args:
            database: Database instance for storing energy data
            idle_baseline_w: Default idle power baseline in watts
        """
        self.database = database
        # Load cost rate from database (persisted user setting)
        self.cost_rate = self.database.get_cost_rate()
        self.idle_baseline_w = idle_baseline_w

        # Session tracking
        self.session_start = None
        self.last_update = None
        self.total_energy_wh = 0.0
        self.gpu_energy_wh = 0.0
        self.cpu_energy_wh = 0.0

    def start_session(self) -> None:
        """Start a new energy tracking session."""
        self.session_start = datetime.now().isoformat()
        self.last_update = self.session_start
        self.total_energy_wh = 0.0
        self.gpu_energy_wh = 0.0
        self.cpu_energy_wh = 0.0

        # Initialize cumulative energy in database
        self.database.update_cumulative_energy(
            session_start=self.session_start,
            total_wh=0.0,
            gpu_wh=0.0,
            cpu_wh=0.0,
            session_cost_usd=0.0,
        )

    def stop_session(self) -> Dict[str, Any]:
        """Stop current session and return final stats.

        Returns:
            Dictionary with session statistics
        """
        if not self.session_start:
            return {"error": "No active session"}

        end_time = datetime.now().isoformat()
        session_cost = self.calculate_cost(self.total_energy_wh)

        # Update cumulative energy
        self.database.update_cumulative_energy(
            session_start=self.session_start,
            total_wh=self.total_energy_wh,
            gpu_wh=self.gpu_energy_wh,
            cpu_wh=self.cpu_energy_wh,
            session_cost_usd=session_cost,
        )

        # Close session in sessions table
        cursor = self.database.conn.cursor()
        cursor.execute(
            """
            UPDATE sessions
            SET end_time = ?, total_gpu_wh = ?, total_cpu_wh = ?, total_cost_usd = ?
            WHERE start_time = ?
            """,
            (end_time, self.gpu_energy_wh, self.cpu_energy_wh, session_cost, self.session_start),
        )
        self.database.conn.commit()

        result = {
            "session_start": self.session_start,
            "session_end": end_time,
            "total_wh": self.total_energy_wh,
            "gpu_wh": self.gpu_energy_wh,
            "cpu_wh": self.cpu_energy_wh,
            "total_cost_usd": session_cost,
        }

        # Reset session state
        self.session_start = None
        self.last_update = None
        self.total_energy_wh = 0.0
        self.gpu_energy_wh = 0.0
        self.cpu_energy_wh = 0.0

        return result

    def calculate_power_cost(
        self,
        gpu_power_w: float,
        cpu_power_w: float,
        duration_seconds: float,
    ) -> Dict[str, Any]:
        """Calculate cost for given power consumption over time.

        Args:
            gpu_power_w: GPU power in watts
            cpu_power_w: CPU power in watts
            duration_seconds: Duration in seconds

        Returns:
            Dictionary with power and cost data
        """
        # Calculate energy in watt-hours
        duration_hours = duration_seconds / 3600.0
        gpu_energy_wh = gpu_power_w * duration_hours
        cpu_energy_wh = cpu_power_w * duration_hours
        total_energy_wh = gpu_energy_wh + cpu_energy_wh

        # Calculate cost
        cost_usd = self.calculate_cost(total_energy_wh)

        return {
            "gpu_power_w": gpu_power_w,
            "cpu_power_w": cpu_power_w,
            "duration_seconds": duration_seconds,
            "duration_hours": duration_hours,
            "gpu_wh": gpu_energy_wh,
            "cpu_wh": cpu_energy_wh,
            "total_wh": total_energy_wh,
            "cost_usd": cost_usd,
        }

    def calculate_cost(self, energy_wh: float) -> float:
        """Calculate cost for energy consumption.

        Args:
            energy_wh: Energy in watt-hours

        Returns:
            Cost in USD
        """
        energy_kwh = energy_wh / 1000.0
        return energy_kwh * self.cost_rate

    def update_power_readings(
        self,
        gpu_power_w: float,
        cpu_power_w: float,
        duration_seconds: float,
    ) -> Dict[str, Any]:
        """Update power readings and recalculate totals.

        Args:
            gpu_power_w: Current GPU power in watts
            cpu_power_w: Current CPU power in watts
            duration_seconds: Time since last update in seconds

        Returns:
            Dictionary with updated energy totals
        """
        if not self.session_start:
            self.start_session()

        # Calculate energy added this interval
        duration_hours = duration_seconds / 3600.0
        gpu_energy = gpu_power_w * duration_hours
        cpu_energy = cpu_power_w * duration_hours
        total_energy = gpu_energy + cpu_energy

        # Update running totals
        self.gpu_energy_wh += gpu_energy
        self.cpu_energy_wh += cpu_energy
        self.total_energy_wh += total_energy

        # Update timestamp
        self.last_update = datetime.now().isoformat()

        # Update database
        session_cost = self.calculate_cost(self.total_energy_wh)
        self.database.update_cumulative_energy(
            session_start=self.session_start,
            total_wh=self.total_energy_wh,
            gpu_wh=self.gpu_energy_wh,
            cpu_wh=self.cpu_energy_wh,
            session_cost_usd=session_cost,
        )

        return {
            "total_wh": self.total_energy_wh,
            "gpu_wh": self.gpu_energy_wh,
            "cpu_wh": self.cpu_energy_wh,
            "total_cost_usd": session_cost,
        }

    def calculate_idle_baseline(
        self,
        cpu_percent: float,
        gpu_percent: float,
        system_power_w: float,
    ) -> Optional[float]:
        """Calculate idle baseline power when system is idle.

        Args:
            cpu_percent: CPU utilization percentage
            gpu_percent: GPU utilization percentage
            system_power_w: Measured system power in watts

        Returns:
            Idle baseline power if conditions met, None otherwise
        """
        # System is idle when CPU + GPU < 5%
        if cpu_percent + gpu_percent < 5.0:
            return system_power_w
        return None

    def format_cost_display(
        self,
        total_wh: float,
        duration_seconds: float,
        rate: float = None,
    ) -> str:
        """Format cost for display.

        Args:
            total_wh: Total energy in watt-hours
            duration_seconds: Duration in seconds
            rate: Optional override for cost rate

        Returns:
            Formatted cost string
        """
        rate = rate or self.cost_rate
        cost = self.calculate_cost(total_wh)

        hours = duration_seconds / 3600.0
        minutes = duration_seconds / 60.0

        if hours >= 1:
            time_str = f"{hours:.1f} hours"
        elif minutes >= 1:
            time_str = f"{minutes:.0f} minutes"
        else:
            time_str = f"{duration_seconds:.0f} seconds"

        return f"${cost:.4f} ({time_str} @ ${rate:.2f}/kWh)"

    def get_session_stats(self) -> Optional[Dict[str, Any]]:
        """Get current session statistics.

        Returns:
            Dictionary with session stats or None
        """
        if not self.session_start:
            return None

        cursor = self.database.conn.cursor()
        cursor.execute(
            """
            SELECT session_start, last_update, total_wh, gpu_wh, cpu_wh, session_cost_usd
            FROM cumulative_energy
            WHERE id = 1
            """
        )
        row = cursor.fetchone()
        if row:
            return {
                "session_start": row["session_start"],
                "last_update": row["last_update"],
                "total_wh": row["total_wh"],
                "gpu_wh": row["gpu_wh"],
                "cpu_wh": row["cpu_wh"],
                "session_cost_usd": row["session_cost_usd"],
            }
        return None

    def set_cost_rate(self, rate: float) -> None:
        """Update the cost rate in the database.

        Args:
            rate: New cost rate in USD per kWh
        """
        self.database.set_cost_rate(rate)
        self.cost_rate = rate


if __name__ == "__main__":
    # Test the calculator
    db = Database(":memory:")
    with db:
        calculator = ElectricityCostCalculator(db, cost_rate=0.12)

        # Start a session
        calculator.start_session()

        # Simulate some power readings
        for i in range(5):
            time.sleep(1)
            stats = calculator.update_power_readings(
                gpu_power_w=250.0,
                cpu_power_w=65.0,
                duration_seconds=1.0,
            )
            print(f"Session {i+1}: {calculator.format_cost_display(stats['total_wh'], (i+1))}")

        # Stop session
        final = calculator.stop_session()
        print(f"\nFinal Session Stats:")
        print(f"  Total: {final['total_wh']:.2f} Wh")
        print(f"  GPU:   {final['gpu_wh']:.2f} Wh")
        print(f"  CPU:   {final['cpu_wh']:.2f} Wh")
        print(f"  Cost:  ${final['total_cost_usd']:.4f}")
