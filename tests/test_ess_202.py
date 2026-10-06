"""ESS-202: the same EMPID cannot be added twice."""
import unittest

from app.user_service import UserService


class Ess202DuplicateEmpidTests(unittest.TestCase):
    def setUp(self):
        self.svc = UserService()
        self.svc.add_user("EMP2", "ravi", "Tester")

    def test_duplicate_empid_raises(self):
        with self.assertRaisesRegex(ValueError, "^EMPID EMP2 already exists$"):
            self.svc.add_user("EMP2", "other", "Developer")

    def test_list_unchanged_after_rejected_add(self):
        before = self.svc.list_users()
        with self.assertRaises(ValueError):
            self.svc.add_user("EMP2", "other", "Developer")
        self.assertEqual(self.svc.list_users(), before)

    def test_new_empid_still_added(self):
        self.svc.add_user("EMP3", "meera", "Developer")
        self.assertEqual([u["empid"] for u in self.svc.list_users()], ["EMP2", "EMP3"])


if __name__ == "__main__":
    unittest.main()
