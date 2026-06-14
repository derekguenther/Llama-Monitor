@echo off
echo WARNING: This will instantly erase the last Git commit the agent made and restore your files to the previous state.
pause
wsl -d Ubuntu-24.04 -e bash -c "cd /mnt/c/Users/ClaudeCode/Documents/llama-monitor && git revert HEAD --no-edit"
echo.
echo The agent's last commit has been undone. Your project is safe!
pause