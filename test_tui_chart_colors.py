"""Tests for tui.py history chart color distinctness and legend (9kf.17).

Verifies:
1. GPU and Power use DISTINCT colors (previously both used 'cost' = magenta).
2. The legend text reflects the actual colors.
3. GPU/CPU/Power charts do not overlap in row positions.
"""
import unittest
import os
import re


TUI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tui.py")


def read_tui():
    with open(TUI_PATH) as f:
        return f.read()


class HistoryChartColorTest(unittest.TestCase):

    def setUp(self):
        self.src = read_tui()

    def test_power_color_is_distinct_from_gpu(self):
        # GPU chart uses self.colors.get("cost")
        self.assertIn('"GPU:", self.colors.get("cost")', self.src)
        # Power chart uses self.colors.get("power") (distinct, not cost)
        self.assertIn('"Power:", self.colors.get("power")', self.src)
        self.assertIn('stdscr.addstr(power_label_row + 1 + i, 7, "=" * bar_width, self.colors.get("power"))',
                      self.src)

    def test_gpu_and_power_use_different_color_keys(self):
        # GPU bars use "cost"; Power bars use "power" (distinct)
        self.assertIn('self.colors.get("cost"))', self.src)
        self.assertIn('self.colors.get("power"))', self.src)
        # GPU label uses cost, power label uses power
        self.assertIn('"GPU:", self.colors.get("cost")', self.src)
        self.assertIn('"Power:", self.colors.get("power")', self.src)

    def test_power_color_pair_defined(self):
        # A dedicated color pair (9) is defined for power
        self.assertIn("curses.init_pair(9, curses.COLOR_CYAN, -1)", self.src)
        # And it's mapped into the colors dict
        self.assertIn('"power": curses.color_pair(9)', self.src)

    def test_legend_reflects_actual_colors(self):
        # Legend must say GPU = magenta, CPU = green, Power = cyan
        self.assertIn("Legend: GPU = magenta, CPU = green, Power = cyan", self.src)

    def test_cpu_and_power_no_overlap_with_gpu(self):
        # CPU label row and Power label row must be below GPU's bar region.
        # GPU bars span row+1 .. row+chart_height (8 rows).
        # CPU label must be at row+chart_height+1 (below GPU bars).
        self.assertIn("cpu_label_row = row + chart_height + 1", self.src)
        # Power label must be below CPU's bars (cpu_label_row + 4)
        self.assertIn("power_label_row = cpu_label_row + 4", self.src)

    def test_legend_does_not_claim_wrong_colors(self):
        # The legend should NOT claim GPU is green or CPU is blue
        self.assertNotIn("GPU = green", self.src)
        self.assertNotIn("CPU = blue", self.src)


if __name__ == "__main__":
    unittest.main()
