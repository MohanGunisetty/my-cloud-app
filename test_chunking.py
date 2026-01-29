import os
import unittest
from chunker import read_in_chunks, CHUNK_SIZE

class TestChunking(unittest.TestCase):
    def setUp(self):
        # Create a dummy file larger than 1 chunk (e.g. 50MB) if possible, 
        # but for speed we will mock or use a smaller chunk size for testing logic
        self.test_file = "test_large.bin"
        # We'll simulate a 50MB file
        with open(self.test_file, "wb") as f:
            f.write(os.urandom(50 * 1024 * 1024)) # 50 MB

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_chunk_splitting(self):
        print(f"\nTesting split of 50MB file with {CHUNK_SIZE/1024/1024}MB chunk size...")
        
        chunk_count = 0
        total_bytes = 0
        
        with open(self.test_file, "rb") as f:
            for chunk in read_in_chunks(f):
                chunk_count += 1
                total_bytes += len(chunk)
                
                # Verify chunk size
                if chunk_count == 1:
                    # First chunk should be full 49MB
                    self.assertEqual(len(chunk), CHUNK_SIZE)
                else:
                    # Last chunk is remainder (1MB)
                    self.assertLessEqual(len(chunk), CHUNK_SIZE)

        # 50MB = 49MB + 1MB -> 2 chunks
        self.assertEqual(chunk_count, 2)
        self.assertEqual(total_bytes, 50 * 1024 * 1024)
        print("✅ Chunking Logic Verified: 50MB -> 49MB + 1MB")

if __name__ == "__main__":
    unittest.main()
