# workflows

A lightweight network latency monitor that runs locally on macOS and logs ping results to GitHub daily.

## What it does

- Pings `8.8.8.8` (Google DNS) and `1.1.1.1` (Cloudflare DNS) every 8 hours
- Records average round-trip latency for each as **WEST** and **EAST**
- Appends each result to `ping.log`
- Commits and pushes `ping.log` to this repo once a day

## Files

| File | Description |
|------|-------------|
| `ping_check.sh` | Pings both IPs, extracts average latency, appends a timestamped entry to `ping.log` |
| `git_sync.sh` | Commits any new `ping.log` entries and pushes to GitHub |
| `ping.log` | Running log of latency readings |

## Log format

Each line in `ping.log` follows this format:

```
YYYY-MM-DD HH:MM:SS | WEST=<ms>ms | EAST=<ms>ms
```

Example:
```
2026-06-27 20:03:09 | WEST=36.614ms | EAST=46.746ms
```

## Cron schedule

Both scripts are registered in the local macOS crontab:

```
# Ping latency check every 8 hours
0 0,8,16 * * * /Users/cliff/Desktop/Claude_Work/workflows/ping_check.sh

# Push ping.log to GitHub daily at 1am
0 1 * * * /Users/cliff/Desktop/Claude_Work/workflows/git_sync.sh
```

To view the crontab: `crontab -l`

## Setup (if re-cloning)

1. Clone the repo
2. Make the scripts executable:
   ```bash
   chmod +x ping_check.sh git_sync.sh
   ```
3. Update the hardcoded `REPO` and `LOG` paths in both scripts to match your local clone path
4. Register the cron jobs:
   ```bash
   (crontab -l 2>/dev/null; cat <<'EOF'
   0 0,8,16 * * * /path/to/workflows/ping_check.sh
   0 1 * * * /path/to/workflows/git_sync.sh
   EOF
   ) | crontab -
   ```
