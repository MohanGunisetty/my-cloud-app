
# 49 MB - Keeping slightly under Telegram's 50MB limit for bots to be safe
CHUNK_SIZE = 49 * 1024 * 1024 

class Config:
    CHUNK_SIZE = CHUNK_SIZE

def read_in_chunks(file_object, chunk_size=CHUNK_SIZE):
    """
    Generator that reads a file object in chunks.
    Critical for memory efficiency with 1GB+ files.
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def get_chunk_metadata(file_size):
    """
    Calculate how many chunks are expected.
    """
    chunks_needed = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE > 0 else 0)
    return chunks_needed
