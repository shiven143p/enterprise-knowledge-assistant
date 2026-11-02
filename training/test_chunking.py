
from app.backend.services.chunking_service import (
    get_all_chunks
)


def main():

    chunks = get_all_chunks()

    print("Total chunks:", len(chunks))

    for chunk in chunks[:5]:

        print("\n----------------------")
        print("Chunk ID:", chunk["chunk_id"])
        print("Document:", chunk["filename"])
        print("Content:")
        print(chunk["text"])


if __name__ == "__main__":
    main()
