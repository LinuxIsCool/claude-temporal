# claude-temporal

Provides continuous temporal awareness to Claude by injecting timestamps at key conversation events.

## What It Does

Injects timestamps into Claude's visible context at:

| Event | When | Example Output |
|-------|------|----------------|
| `SessionStart` | Conversation begins | `[2026-03-03 08:59:25 PST] SessionStart - Monday (morning)` |
| `UserPromptSubmit` | User sends message | `[2026-03-03 09:00:15 PST] UserPromptSubmit` |
| `Stop` | Claude finishes response | `[2026-03-03 09:01:02 PST] Stop` |
| `SessionEnd` | Conversation ends | `[2026-03-03 09:30:00 PST] SessionEnd` |

## Why

Without this plugin, Claude has no reliable way to know the current time. This leads to:
- Guessing timestamps for journal entries
- Inability to reason about "now" vs scheduled events
- No awareness of session duration

With this plugin, Claude sees an **interaction timeline** throughout the conversation.

## Installation

```bash
claude plugin add /path/to/claude-temporal
```

## Context Cost

Each timestamp injection is ~15-20 tokens. For a typical 20-exchange session, this adds ~400-500 tokens total — negligible compared to the value of temporal grounding.

## Architecture

```
claude-temporal/
├── .claude-plugin/
│   └── plugin.json          # Hook registrations (4 events)
├── hooks/
│   └── inject_timestamp.py  # Timestamp injection (uv inline script)
├── .gitignore
└── README.md
```

No dependencies. No agents. No skills. Just hooks.
