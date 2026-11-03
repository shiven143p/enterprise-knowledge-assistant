
from app.backend.services.sap_vector_service import (
    build_sap_index,
    search_sap_documents
)


print("Indexed chunks:", build_sap_index())

questions = [
    "My vendor invoice cannot be posted.",
    "SAP is showing an incorrect tax amount.",
    "A customer payment is not clearing.",
    "An expense was posted to the wrong cost center."
]

for question in questions:
    print("\nQUESTION:", question)

    results = search_sap_documents(question, top_k=3)

    for rank, result in enumerate(results, start=1):
        print(
            rank,
            result["filename"],
            round(result["distance"], 4)
        )
        print(result["document"][:200])
