#!/usr/bin/env python3
"""PreToolUse debug hook: logs tool input to a timestamped file."""

import json
import os
import sys
from datetime import datetime

LOG_DIR = "/ephemeral/c.dumas/hook_debug_logs"


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    raw = sys.stdin.read()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    data = json.loads(raw)
    tool_name = data.get("tool_name", "unknown")
    log_file = os.path.join(LOG_DIR, f"{ts}_{tool_name}.json")
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
