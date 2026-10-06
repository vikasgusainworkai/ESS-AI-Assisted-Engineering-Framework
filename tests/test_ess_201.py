"""ESS-201: deleting an employee must not delete others whose EMPID starts with the same text."""
import unittest

from app.user_service import UserService


class TestEss201(unittest.TestCase):
    def setUp(self):
        self.service = UserService()
        for empid in ("EMP1", "EMP10", "EMP11"):
            self.service.add_user(empid, f"user {empid}", "Engineer")

    def test_delete_removes_only_exact_empid(self):
        self.service.delete_user("EMP1")
        remaining = [u["empid"] for u in self.service.list_users()]
        self.assertEqual(remaining, ["EMP10", "EMP11"])

    def test_delete_unknown_empid_raises_and_removes_nobody(self):
        with self.assertRaises(KeyError):
            self.service.delete_user("EMP")
        self.assertEqual(len(self.service.list_users()), 3)


if __name__ == "__main__":
    unittest.main()
