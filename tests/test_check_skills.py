import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_skills import check_root, check_skill  # noqa: E402

FIX = ROOT / "tests" / "fixtures"


class CheckSkillsTest(unittest.TestCase):
    def test_good_skill_passes(self):
        self.assertEqual(check_skill(FIX / "good", None), [])

    def test_name_mismatch(self):
        self.assertIn("name 'other' != folder 'bad-name'", check_skill(FIX / "bad-name", None))

    def test_missing_reference(self):
        self.assertIn("missing references/block9-x.md", check_skill(FIX / "missing-ref", None))

    def test_expected_skill_missing(self):
        self.assertIn("mom-x: missing SKILL.md", check_root(FIX, expect=["mom-x"]))

    def test_common_rules_required(self):
        self.assertIn("common rules not included", check_skill(FIX / "good", "이 문장은 없다"))


if __name__ == "__main__":
    unittest.main()
