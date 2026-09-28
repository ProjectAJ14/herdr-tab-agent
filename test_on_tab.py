import os
import tempfile
import unittest

import on_tab

TAB = {"tab_id": "w1:t2", "workspace_id": "w1"}
TABS = [{"tab_id": "w1:t1", "workspace_id": "w1"}, TAB]


class TargetPane(unittest.TestCase):
    def test_fresh_tab(self):
        panes = [{"pane_id": "w1:p1", "tab_id": "w1:t1", "agent": "claude"},
                 {"pane_id": "w1:p2", "tab_id": "w1:t2"}]
        self.assertEqual(on_tab.target_pane(TAB, TABS, panes), "w1:p2")

    def test_tab_with_agent_is_left_alone(self):
        panes = [{"pane_id": "w1:p2", "tab_id": "w1:t2", "agent": "claude"}]
        self.assertIsNone(on_tab.target_pane(TAB, TABS, panes))

    def test_restored_multi_pane_tab_is_left_alone(self):
        panes = [{"pane_id": "w1:p2", "tab_id": "w1:t2"},
                 {"pane_id": "w1:p3", "tab_id": "w1:t2"}]
        self.assertIsNone(on_tab.target_pane(TAB, TABS, panes))

    def test_first_tab_of_workspace_stays_a_shell(self):
        panes = [{"pane_id": "w1:p2", "tab_id": "w1:t2"}]
        self.assertIsNone(on_tab.target_pane(TAB, [TAB], panes))


class AgentCommand(unittest.TestCase):
    def test_default(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["HERDR_PLUGIN_CONFIG_DIR"] = d
            self.assertEqual(on_tab.agent_command(), "claude")

    def test_config_file(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "command"), "w") as f:
                f.write("# my agent\n\ncodex --full-auto\n")
            os.environ["HERDR_PLUGIN_CONFIG_DIR"] = d
            self.assertEqual(on_tab.agent_command(), "codex --full-auto")


if __name__ == "__main__":
    unittest.main()
