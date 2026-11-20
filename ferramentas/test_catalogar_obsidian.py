"""Testes isolados: nunca usam o cofre real como destino de gravação."""

from pathlib import Path
import os
import tempfile
import unittest

import catalogar_obsidian as catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "Temp" / "opencode"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="catalogo-test-", dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "origem"
        self.source.mkdir()
        self.output = self.root / "cofre" / catalog.FOLDER

    def skill(self, relative, name="example", description="Uma tarefa específica.", body="# Instruções\n\nPreservar os arquivos existentes."):
        path = self.source / relative / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\ndescription: {description}\n---\n\n{body}\n", encoding="utf-8")
        return path

    def test_parse_frontmatter(self):
        path = self.skill("skills-do-artigo/example")
        metadata, body, raw = catalog.parse_skill(path)
        self.assertEqual(metadata["name"], "example")
        self.assertIn("Preservar", body)
        self.assertEqual(raw, path.read_bytes())

    def test_parse_bom_crlf_and_folded_description(self):
        path = self.source / "SKILL.md"
        path.write_bytes("\ufeff---\r\nname: example\r\ndescription: >\r\n  Primeira linha\r\n  segunda linha\r\n---\r\n# Fluxo\r\n".encode("utf-8"))
        metadata, body, _ = catalog.parse_skill(path)
        self.assertEqual(catalog.compact(metadata["description"]), "Primeira linha segunda linha")
        self.assertIn("# Fluxo", body)

    def test_missing_metadata_is_rejected(self):
        path = self.source / "SKILL.md"
        path.write_text("# Sem frontmatter", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Frontmatter"):
            catalog.parse_skill(path)

    def test_unsafe_yaml_is_rejected(self):
        path = self.source / "SKILL.md"
        path.write_text("---\nname: example\ndescription: !!python/object:example.Class {}\n---\nTexto", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "YAML inválido"):
            catalog.parse_skill(path)

    def test_metadata_requires_strings(self):
        path = self.skill("skills-do-artigo/example", description="42")
        with self.assertRaisesRegex(ValueError, "description"):
            catalog.parse_skill(path)

    def test_name_and_folder_warnings(self):
        warnings = catalog.metadata_warnings({"name": "-bad", "description": "Descrição"}, "other", "Fluxo")
        self.assertEqual(len(warnings), 2)

    def test_duplicate_names_have_distinct_note_paths(self):
        self.skill("skills-do-artigo/shared", name="shared")
        self.skill("awesome-codex-skills/shared", name="shared")
        records = catalog.collect_records(self.source)
        self.assertEqual(len(records), 2)
        self.assertEqual({record["name"] for record in records}, {"shared"})
        self.assertEqual(len({record["note"] for record in records}), 2)

    def test_nested_plugin_copy_remains_separate(self):
        self.skill("skills-do-artigo/slides", name="slides")
        self.skill("skills-do-artigo/slides/plugins/slides/skills/slides", name="slides")
        records = catalog.collect_records(self.source)
        self.assertEqual(len(records), 2)
        self.assertTrue(any("/plugins/" in record["note"] for record in records))

    def test_invalid_custom_skill_stops_generation(self):
        self.skill("skills-personalizadas/-bad", name="-bad")
        with self.assertRaisesRegex(ValueError, "personalizada inválida"):
            catalog.collect_records(self.source)

    def test_source_is_not_modified(self):
        path = self.skill("skills-do-artigo/example")
        before = path.read_bytes()
        catalog.collect_records(self.source)
        self.assertEqual(path.read_bytes(), before)

    def test_table_wikilink_escapes_alias_separator(self):
        self.skill("skills-do-artigo/example")
        notes = catalog.render_catalog(catalog.collect_records(self.source), self.source, {}, "2026-11-18")
        self.assertIn("example\\|example]]", notes["01 - Catalogo completo.md"])

    def test_invalid_name_is_not_offered_as_invocation(self):
        self.skill("awesome-codex-skills/composio-skills/-21risk-automation", name="-21risk-automation")
        record = catalog.collect_records(self.source)[0]
        text = catalog.render_skill(record, [], {})
        self.assertNotIn("$-21risk-automation", text)
        self.assertIn("Revisar antes de usar", text)

    def test_app_labels_preserve_brand_and_strip_automation_suffix(self):
        self.assertEqual(catalog.app_name("Ahrefs Automation", "SEO research."), "Ahrefs")
        self.assertEqual(catalog.app_name("google_maps-automation", "Map tools."), "google maps")
        self.assertEqual(catalog.app_name("ably-automation", "Automate Ably tasks via a service."), "Ably")

    def test_dry_run_writes_nothing(self):
        result = catalog.apply_notes(self.output, {"A.md": "Conteúdo\n"}, False, "2026-11-18")
        self.assertEqual(result["pending_files"], 2)
        self.assertFalse(self.output.exists())

    def test_generation_is_idempotent(self):
        notes = {"A.md": "Conteúdo\n", "Pasta/B.md": "Outra nota\n"}
        catalog.apply_notes(self.output, notes, True, "2026-11-18")
        result = catalog.apply_notes(self.output, notes, False, "2026-11-18")
        self.assertEqual(result["pending_files"], 0)

    def test_managed_unedited_file_can_be_updated(self):
        catalog.apply_notes(self.output, {"A.md": "Versão 1\n"}, True, "2026-11-18")
        catalog.apply_notes(self.output, {"A.md": "Versão 2\n"}, True, "2026-11-18")
        self.assertEqual((self.output / "A.md").read_text(encoding="utf-8"), "Versão 2\n")

    def test_manual_edit_prevents_all_initial_writes(self):
        catalog.apply_notes(self.output, {"A.md": "Gerado\n"}, True, "2026-11-18")
        (self.output / "A.md").write_text("Texto do usuário\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "preservados"):
            catalog.apply_notes(self.output, {"A.md": "Atualização\n", "B.md": "Novo\n"}, True, "2026-11-18")
        self.assertFalse((self.output / "B.md").exists())
        self.assertEqual((self.output / "A.md").read_text(encoding="utf-8"), "Texto do usuário\n")

    def test_existing_unmanaged_file_is_preserved(self):
        self.output.mkdir(parents=True)
        (self.output / "A.md").write_text("Original", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Conflitos"):
            catalog.apply_notes(self.output, {"A.md": "Gerado"}, True, "2026-11-18")
        self.assertEqual((self.output / "A.md").read_text(encoding="utf-8"), "Original")

    def test_stale_files_are_not_deleted(self):
        catalog.apply_notes(self.output, {"A.md": "A", "B.md": "B"}, True, "2026-11-18")
        result = catalog.apply_notes(self.output, {"A.md": "A"}, True, "2026-11-18")
        self.assertEqual(result["preserved_stale_paths"], ["B.md"])
        self.assertEqual((self.output / "B.md").read_text(encoding="utf-8"), "B")

    def test_path_traversal_is_rejected(self):
        for relative in ("../fora.md", "/fora.md", "Pasta/../../fora.md", "C:/fora.md", "Pasta\\fora.md"):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                catalog.safe_target(self.output, relative)

    def test_case_insensitive_collisions_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Colisão"):
            catalog.apply_notes(self.output, {"A.md": "A", "a.md": "a"}, True, "2026-11-18")
        self.assertFalse(self.output.exists())

    def test_unknown_manifest_is_preserved(self):
        manifest = self.output / catalog.MANIFEST
        manifest.parent.mkdir(parents=True)
        manifest.write_text('{"generator": "outro", "files": {}}', encoding="utf-8")
        before = manifest.read_bytes()
        with self.assertRaisesRegex(ValueError, "Manifesto desconhecido"):
            catalog.apply_notes(self.output, {"A.md": "A"}, True, "2026-11-18")
        self.assertEqual(manifest.read_bytes(), before)

    def test_authored_custom_skills_have_valid_structure(self):
        source = Path(catalog.__file__).resolve().parents[1]
        paths = list((source / "skills-personalizadas").glob("*/SKILL.md"))
        self.assertEqual(len(paths), 3)
        for path in paths:
            with self.subTest(skill=path.parent.name):
                metadata, body, _ = catalog.parse_skill(path)
                self.assertEqual(set(metadata), {"name", "description"})
                self.assertEqual(catalog.metadata_warnings(metadata, path.parent.name, body), [])
                self.assertLess(len(body.splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
