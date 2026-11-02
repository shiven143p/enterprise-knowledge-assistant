from app.backend.services.vector_service import (
    search_documents
)


def main():

    queries = [
        "How much paid vacation do employees receive?",
        "What should I do if my VPN stops working?",
        "When will my approved expenses be paid?",
        "Can I fly business class on a domestic work trip?"
    ]

    for query in queries:

        print("\n" + "=" * 60)
        print("QUERY:", query)

        matches = search_documents(
            query=query,
            top_k=3
        )

        for rank, match in enumerate(matches, start=1):

            print(f"\nResult {rank}")
            print("Document:", match["filename"])
            print("Distance:", match["distance"])
            print("Passage:")
            print(match["document"])


if __name__ == "__main__":
    main()
