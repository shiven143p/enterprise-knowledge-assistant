
from app.backend.services.llm_service import (
    generate_response
)


def main():
    answer = generate_response(
        prompt=(
            "Explain Retrieval-Augmented Generation "
            "in two simple sentences."
        ),
        system_instruction=(
            "You are a helpful AI engineering tutor."
        )
    )

    print("Gemini response:")
    print(answer)


if __name__ == "__main__":
    main()
