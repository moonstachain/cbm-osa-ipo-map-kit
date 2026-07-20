import ast
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "ops/card_triangle_scorer.py"


class LegacyRetirementTest(unittest.TestCase):
    def test_cli_fails_closed_with_machine_readable_retirement(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "--all", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "retired")
        self.assertEqual(payload["contract"], "yuanli-osa-card/v2")
        self.assertEqual(
            payload["schema_sha256"],
            "d229df1e18ec8bd1fa2325ec3a1d11f3d124416d839368a5dfe0115e05b91268",
        )

    def test_cli_does_not_import_the_legacy_engine(self):
        tree = ast.parse(CLI.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.rsplit(".", 1)[-1] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").rsplit(".", 1)[-1])
                imported.update(alias.name for alias in node.names)
        self.assertNotIn("legacy_map_engine", imported)
        self.assertNotIn("card_triangle_scorer", imported)


if __name__ == "__main__":
    unittest.main()
