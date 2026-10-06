"""ESS-203: blank or space-only values are rejected; values are trimmed."""
import unittest

from app.user_service import UserService


class Ess203BlankValueTests(unittest.TestCase):
    def setUp(self):
        self.svc = UserService()

    def test_blank_or_missing_fields_rejected_on_add(self):
        cases = [
            (("   ", "asha", "Developer"), "EMPID is required"),
            (("EMP1", "   ", "Developer"), "Username is required"),
            (("EMP1", "asha", ""), "Designation is required"),
            (("EMP1", None, "Developer"), "Username is required"),
        ]
        for args, message in cases:
            with self.subTest(args=args):
                with self.assertRaisesRegex(ValueError, f"^{message}$"):
                    self.svc.add_user(*args)
        self.assertEqual(self.svc.list_users(), [])

    def test_values_trimmed_on_add(self):
        self.svc.add_user("  EMP1 ", "  asha  ", " Developer ")
        self.assertEqual(self.svc.list_users(), [{"empid": "EMP1", "username": "asha", "designation": "Developer"}])

    def test_same_rules_on_edit(self):
        self.svc.add_user("EMP1", "asha", "Developer")
        with self.assertRaisesRegex(ValueError, "^Username is required$"):
            self.svc.update_user("EMP1", "   ", "Tech Lead")
        self.svc.update_user("EMP1", " asha.rao ", "  Tech Lead ")
        self.assertEqual(self.svc.get_user("EMP1"), {"empid": "EMP1", "username": "asha.rao", "designation": "Tech Lead"})


if __name__ == "__main__":
    unittest.main()
