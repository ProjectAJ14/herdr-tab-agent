"""tab.created hook: run the configured agent in the new tab's only pane."""
import json
import os
import subprocess

DEFAULT_COMMAND = "claude"
HERDR = os.environ.get("HERDR_BIN_PATH") or "herdr"


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


def target_pane(tab, tabs, panes):
    """The tab's pane, if it is a fresh one-pane tab with no agent in it.

    A workspace's first tab stays a shell, and restored tabs and tabs another
    tool already filled are left alone.
    """
    if sum(t.get("workspace_id") == tab["workspace_id"] for t in tabs) < 2:
        return None
    mine = [p for p in panes if p.get("tab_id") == tab["tab_id"]]
    if len(mine) == 1 and not mine[0].get("agent"):
        return mine[0]["pane_id"]
    return None


def shell_is_idle(info):
    """True when the pane's shell is at its prompt, not running a command.

    A pane moved into a new tab also fires tab.created, possibly mid-command;
    typing into it would queue the agent behind whatever it runs.
    """
    return info.get("foreground_process_group_id") == info.get("shell_pid")


def herdr(*args):
    out = subprocess.run(
        [HERDR, *args], capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)["result"]


def main():
    tab = json.loads(os.environ["HERDR_PLUGIN_EVENT_JSON"])["data"]["tab"]
    tabs = herdr("tab", "list", "--workspace", tab["workspace_id"])["tabs"]
    panes = herdr("pane", "list", "--workspace", tab["workspace_id"])["panes"]
    pane = target_pane(tab, tabs, panes)
    if pane and shell_is_idle(herdr("pane", "process-info", "--pane", pane)["process_info"]):
        herdr("pane", "run", pane, agent_command())


if __name__ == "__main__":
    main()
