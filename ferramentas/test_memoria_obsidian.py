import tempfile
import unittest
from pathlib import Path

from memoria_obsidian import ALLOWED_NOTES, search, tokens


class MemorySearchTests(unittest.TestCase):
    def test_accents_and_case(self):
        self.assertEqual(tokens('DECISÃO memória'), tokens('decisao MEMORIA'))

    def test_scope_citations_ranking_and_read_only(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            note = root / ALLOWED_NOTES[0]
            content = 'Logo aprovada\nSegunda imagem roxa\n' + '\n' * 12 + 'Outro assunto'
            note.write_text(content, encoding='utf-8')
            (root / 'privado.md').write_text('logo segunda imagem', encoding='utf-8')
            results = search(root, 'logo segunda imagem', limit=1)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['source'], str(note))
            self.assertEqual(results[0]['line_start'], 1)
            self.assertEqual(results[0]['score'], 3)
            self.assertEqual(note.read_text(encoding='utf-8'), content)
            self.assertEqual(search(root, 'inexistente'), [])


if __name__ == '__main__':
    unittest.main()
