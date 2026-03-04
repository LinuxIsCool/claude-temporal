# claude-temporal

Continuous temporal awareness for Claude Code via hook-injected timestamps.

## What It Does

Injects timestamps at key conversation events so Claude always knows what time it is.

| Event | Output Type | User Visible | Claude Visible | Example |
|-------|------------|:---:|:---:|---------|
| `SessionStart` | systemMessage + additionalContext | yes | yes | `Tuesday, 2026-03-03 23:07 PDT (night)` |
| `UserPromptSubmit` | additionalContext | no | yes | `2026-03-03 23:08 PDT` |
| `Notification` | additionalContext | no | yes | `2026-03-03 23:09 PDT` |
| `Stop` | systemMessage | yes | no | `2026-03-03 23:10 PDT` |
| `SessionEnd` | systemMessage | yes | no | `2026-03-03 23:30 PDT` |

## Why

Without this plugin, Claude has no reliable way to know the current time. This leads to:
- Guessing timestamps for journal entries
- Inability to reason about "now" vs scheduled events
- No awareness of session duration

With this plugin, Claude sees an **interaction timeline** throughout the conversation.

## Installation

### From GitHub

```bash
claude plugin marketplace add LinuxIsCool/claude-temporal
claude plugin install claude-temporal@claude-temporal
```

### Update

```bash
claude plugin marketplace update claude-temporal
claude plugin update claude-temporal@claude-temporal
```

### From Source

```bash
git clone https://github.com/LinuxIsCool/claude-temporal.git
cd claude-temporal
claude plugin enable .          # project-specific
claude plugin enable --global . # or system-wide
```

## Requirements

- [uv](https://docs.astral.sh/uv/) (for inline script execution)
- Python 3.11+ (no additional dependencies)

## Context Cost

Each timestamp injection is ~15-20 tokens. For a typical 20-exchange session, this adds ~400-500 tokens total — negligible compared to the value of temporal grounding.

## Architecture

```
claude-temporal/
├── .claude-plugin/
│   └── plugin.json          # Hook registrations (5 events)
├── hooks/
│   └── inject_timestamp.py  # Timestamp injection (uv inline script, 0 deps)
├── .gitignore
├── LICENSE
└── README.md
```

No dependencies. No agents. No skills. Just hooks.

## License

MIT
