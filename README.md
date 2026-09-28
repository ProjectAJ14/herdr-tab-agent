# Tab Agent for Herdr

[![CI](https://github.com/ProjectAJ14/herdr-tab-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/ProjectAJ14/herdr-tab-agent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A [Herdr](https://herdr.dev) plugin that makes every **new tab** open straight
into a coding agent (Claude Code by default), while a workspace's **first tab**
and all **split panes** stay plain shells.

```
new workspace (its first tab)       →  ordinary shell
prefix+c / "+" / herdr tab create   →  new tab running `claude`
prefix+v / prefix+minus (split)     →  new pane, ordinary shell
```

## Install

Needs Herdr 0.8.0+ and `python3` on your `PATH` (macOS and Linux).

```sh
herdr plugin install ProjectAJ14/herdr-tab-agent
```

It takes effect on the next tab you open, with no restart needed.

## Pick a different agent

By default it runs `claude`. To run something else, put the command on the first
line of a `command` file in the plugin's config directory:

```sh
echo "codex" > "$(herdr plugin config-dir herdr.tab-agent)/command"
```

Arguments are allowed (`claude --model sonnet`). Blank lines and `#` comments
are skipped.

## How it works

The plugin subscribes to Herdr's `tab.created` event. When it fires, it looks up
the new tab's panes and runs the agent command in the pane with `herdr pane run`.
Splits raise pane events rather than `tab.created`, so they never trigger it.

It leaves a tab alone if it is the only tab in its workspace, has more than one
pane, or already has an agent in it. That keeps it from starting a second agent in a tab that session
restore brought back with `resume_agents_on_restore`.

## Turn it off

```sh
herdr plugin disable herdr.tab-agent     # keep it installed, stop it firing
herdr plugin uninstall herdr.tab-agent   # remove it
```

## Develop

```sh
herdr plugin link .                  # run your checkout instead of the release
python3 -m unittest -v test_on_tab
herdr plugin log list --plugin herdr.tab-agent --limit 5
```

## License

MIT
