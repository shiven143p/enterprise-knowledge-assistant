
from app.backend.services.vector_service import (
    build_vector_database
)


def main():
    print("Building enterprise vector database...")

    result = build_vector_database()

    print("\nIndexing completed.")
    print("Indexed chunks:", result["indexed_chunks"])
    print("Collection count:", result["collection_count"])


if __name__ == "__main__":
    main()
