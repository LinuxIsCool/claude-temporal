#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Temporal plugin hook: Injects timestamps into Claude's context at key events.

- SessionStart, Stop, SessionEnd → systemMessage (visible to user)
- UserPromptSubmit, Notification → additionalContext (quiet injection for Claude)
"""

import argparse
import json
import sys
from datetime import datetime
import time


def get_temporal_context():
    """Generate temporal context."""
    now = datetime.now()

    hour = now.hour
    if 5 <= hour < 12:
        period = "morning"
    elif 12 <= hour < 17:
        period = "afternoon"
    elif 17 <= hour < 21:
        period = "evening"
    else:
        period = "night"

    return {
        "timestamp": now.strftime("%Y-%m-%d %H:%M"),
        "date": now.strftime("%Y-%m-%d"),
        "weekday": now.strftime("%A"),
        "timezone": time.tzname[time.daylight] if time.daylight else time.tzname[0],
        "period": period,
        "is_weekend": now.weekday() >= 5,
    }


# Events where user sees the timestamp (systemMessage)
VISIBLE_EVENTS = {"SessionStart", "Stop", "SessionEnd"}

# Events where Claude gets quiet context (additionalContext)
QUIET_EVENTS = {"UserPromptSubmit", "Notification"}


def format_timestamp(event, ctx):
    """Format timestamp string. No event name — Claude Code already labels it."""
    ts = ctx["timestamp"]
    tz = ctx["timezone"]

    if event == "SessionStart":
        return f"[temporal] {ctx['weekday']}, {ts} {tz} ({ctx['period']})"
    else:
        return f"{ts} {tz}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--event", required=True)
    args = parser.parse_args()

    try:
        json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        pass

    ctx = get_temporal_context()
    ts = format_timestamp(args.event, ctx)

    if args.event == "SessionStart":
        # Both: user sees it + Claude has it in context
        output = {
            "systemMessage": ts,
            "hookSpecificOutput": {
                "hookEventName": args.event,
                "additionalContext": ts,
            },
        }
    elif args.event in QUIET_EVENTS:
        output = {
            "hookSpecificOutput": {
                "hookEventName": args.event,
                "additionalContext": ts,
            }
        }
    elif args.event in VISIBLE_EVENTS:
        output = {"systemMessage": ts}
    else:
        output = {"systemMessage": ts}

    print(json.dumps(output))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
