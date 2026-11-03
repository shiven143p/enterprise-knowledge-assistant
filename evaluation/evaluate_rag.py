
import os
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]

TEST_FILE = ROOT / "evaluation" / "rag_test_cases.csv"
OUTPUT_DIR = ROOT / "evaluation" / "results"

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

TOP_K = 4


def call_api(endpoint, payload):
    """Call an API and measure elapsed time."""

    start = time.perf_counter()

    response = requests.post(
        f"{API_BASE_URL}{endpoint}",
        json=payload,
        timeout=120
    )

    latency = time.perf_counter() - start

    response.raise_for_status()

    return response.json(), latency


def retrieval_hit(matches, expected_document, expected_section):
    """Check whether the expected section was retrieved."""

    for match in matches:
        if (
            match.get("filename") == expected_document
            and expected_section.casefold()
            in match.get("document", "").casefold()
        ):
            return True

    return False


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    test_cases = pd.read_csv(
        TEST_FILE,
        keep_default_na=False
    )

    required = {
        "id", "category", "question",
        "expected_document", "expected_section",
        "expected_answer", "answerable"
    }

    if not required.issubset(test_cases.columns):
        raise ValueError("Missing evaluation columns.")

    if len(test_cases) != 28:
        raise ValueError("Expected 28 evaluation questions.")

    records = []

    for _, case in test_cases.iterrows():
        question = case["question"]
        answerable = int(case["answerable"]) == 1

        print(f"\nTesting {case['id']}: {question}")

        record = {
            **case.to_dict(),
            "retrieval_hit": None,
            "retrieval_latency_s": None,
            "chat_latency_s": None,
            "generated_answer": "",
            "retrieved_sources": "",
            "error": ""
        }

        try:
            search_result, search_time = call_api(
                "/api/search",
                {"query": question, "top_k": TOP_K}
            )

            matches = search_result.get("matches", [])

            record["retrieval_latency_s"] = round(
                search_time, 3
            )

            if answerable:
                record["retrieval_hit"] = int(
                    retrieval_hit(
                        matches,
                        case["expected_document"],
                        case["expected_section"]
                    )
                )

            chat_result, chat_time = call_api(
                "/api/chat",
                {"query": question, "top_k": TOP_K}
            )

            record["chat_latency_s"] = round(
                chat_time, 3
            )

            record["generated_answer"] = (
                chat_result.get("answer", "")
            )

            record["retrieved_sources"] = " | ".join(
                source.get("filename", "")
                for source in chat_result.get("sources", [])
            )

            print("Retrieval hit:", record["retrieval_hit"])
            print("Chat latency:", record["chat_latency_s"])
            print("Answer:", record["generated_answer"][:200])

        
        except requests.exceptions.HTTPError as error:
            status_code = (
                error.response.status_code
                if error.response is not None
                else None
            )

            record["error"] = f"HTTP {status_code}"

            print(
                f"Request failed with HTTP status: {status_code}"
            )

        except requests.exceptions.RequestException as error:
            record["error"] = type(error).__name__

            print(
                "Network request failed:",
                type(error).__name__
            )

        except ValueError as error:
            record["error"] = type(error).__name__

            print(
                "Evaluation error:",
                type(error).__name__
            )


        records.append(record)

        # Small delay to reduce request bursts.
        time.sleep(1)

    results = pd.DataFrame(records)

    results.to_csv(
        OUTPUT_DIR / "rag_evaluation_results.csv",
        index=False
    )

    valid_retrieval = results[
        (results["answerable"] == 1)
        & results["retrieval_hit"].notna()
    ]

    successful_chat = results[
        (results["error"] == "")
        & results["chat_latency_s"].notna()
    ]

    print("\n=== RAG EVALUATION SUMMARY ===")

    print("Total questions:", len(results))
    print("Successful chat requests:", len(successful_chat))
    print("Failed requests:", (results["error"] != "").sum())

    if len(valid_retrieval):
        recall = valid_retrieval["retrieval_hit"].astype(float).mean()
        print(f"Retrieval Hit@{TOP_K}: {recall:.4f}")
        print(
            "Retrieval cases evaluated:",
            len(valid_retrieval),
            "of 24 answerable questions"
        )

    if len(successful_chat):
        print(
            "Average chat latency:",
            round(successful_chat["chat_latency_s"].mean(), 3),
            "seconds"
        )

    print("\nResults saved to:")
    print(OUTPUT_DIR / "rag_evaluation_results.csv")


if __name__ == "__main__":
    main()
