"""tab.created hook: run the configured agent in the new tab's only pane."""
import json
import os
import subprocess

DEFAULT_COMMAND = "claude"


def agent_command():
    """First non-blank line of <config dir>/command, else claude."""
    path = os.path.join(os.environ.get("HERDR_PLUGIN_CONFIG_DIR", ""), "command")
    try:
        with open(path) as f:
            for line in f:
                if line.strip() and not line.lstrip().startswith("#"):
                    return line.strip()
    except OSError:
        pass
    return DEFAULT_COMMAND


def target_pane(tab, panes):
    """The tab's pane, if it is a fresh one-pane tab with no agent in it.

    Restored tabs and tabs another tool already filled are left alone.
    """
    mine = [p for p in panes if p.get("tab_id") == tab["tab_id"]]
    if len(mine) == 1 and not mine[0].get("agent"):
        return mine[0]["pane_id"]
    return None


def main():
    tab = json.loads(os.environ["HERDR_PLUGIN_EVENT_JSON"])["data"]["tab"]
    herdr = os.environ.get("HERDR_BIN_PATH") or "herdr"
    out = subprocess.run(
        [herdr, "pane", "list", "--workspace", tab["workspace_id"]],
        capture_output=True, text=True, check=True,
    ).stdout
    pane = target_pane(tab, json.loads(out)["result"]["panes"])
    if pane:
        subprocess.run([herdr, "pane", "run", pane, agent_command()], check=True)


if __name__ == "__main__":
    main()
