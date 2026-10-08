import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_docs import links, target_path, unclosed_fence, ROOT
from md_mermaid_to_html import escape_mermaid, md_to_html, rewrite_document_links, mermaid_boot_script


class DocsTests(unittest.TestCase):
    def test_code_label_is_still_a_link(self):
        self.assertEqual(list(links('[`workspace`](./folder/)')), [(1, './folder/')])

    def test_code_examples_are_not_links(self):
        text = '```md\n[x](missing.md)\n```\n`[y](also-missing.md)`\n[z](real.md)'
        self.assertEqual(list(links(text)), [(5, 'real.md')])

    def test_unclosed_fence_and_inline_example(self):
        self.assertEqual(unclosed_fence('## Title\n```bash\necho example'), 2)
        self.assertIsNone(unclosed_fence('` ```mermaid ` example\n```bash\necho example\n```'))

    def test_explicit_anchors_are_kept(self):
        self.assertIn('<a id="section"></a>', md_to_html('<a id="section"></a>\n## Title'))

    def test_anchor_is_not_a_local_file(self):
        self.assertIsNone(target_path(ROOT / 'README.md', '#section'))

    def test_mermaid_keeps_html_labels_as_literal_source(self):
        self.assertEqual(escape_mermaid('A["a<br/>b & c"]'), 'A[&quot;a&lt;br/&gt;b &amp; c&quot;]')
        rendered = md_to_html('```mermaid\nflowchart LR\nA["a<br/>b"]\n```')
        self.assertIn('&lt;br/&gt;', rendered)

    def test_nested_source_links_survive_root_output(self):
        output = rewrite_document_links('<a href="./RL.md">RL</a>',
                                        ROOT / 'robotics/edge_deployment.md',
                                        ROOT / 'edge.html')
        self.assertIn('blob/master/robotics/RL.md', output)

    def test_local_first_loading_has_explicit_failure_state(self):
        script = mermaid_boot_script()
        self.assertIn('s.src = "./assets/mermaid/mermaid.min.js"', script)
        self.assertIn('__diagramRenderStatus = "error"', script)


if __name__ == '__main__':
    unittest.main()
