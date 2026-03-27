# launchd notes

Use this pattern on macOS:

```bash
cp <project>/scripts/<plist-name>.plist ~/Library/LaunchAgents/<plist-name>.plist
launchctl unload ~/Library/LaunchAgents/<plist-name>.plist >/dev/null 2>&1 || true
launchctl load ~/Library/LaunchAgents/<plist-name>.plist
launchctl kickstart -k gui/$(id -u)/<label>
```

Recommended settings:
- `StartInterval`: `300`
- `RunAtLoad`: `true`
- set both `StandardOutPath` and `StandardErrorPath`

Always use absolute paths.
launchd PATH is minimal.
