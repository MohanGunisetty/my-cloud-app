import unittest
from auth import hash_password, verify_password_hash

class TestAuth(unittest.TestCase):
    def test_hash_consistency(self):
        # Rule: Same password -> Same hash
        pwd = "my_secure_password_123"
        h1 = hash_password(pwd)
        h2 = hash_password(pwd)
        self.assertEqual(h1, h2)
        print(f"✅ Consistency Check: {h1[:10]}... == {h2[:10]}...")

    def test_hash_uniqueness(self):
        # Rule: Different password -> Different hash
        h1 = hash_password("pass1")
        h2 = hash_password("pass2")
        self.assertNotEqual(h1, h2)
        print("✅ Uniqueness Check: pass1 != pass2")

    def test_verification(self):
        pwd = "secret_login"
        stored = hash_password(pwd)
        self.assertTrue(verify_password_hash(pwd, stored))
        self.assertFalse(verify_password_hash("wrong_login", stored))
        print("✅ Verification Check: Correct/Wrong passwords validated.")

if __name__ == "__main__":
    unittest.main()
