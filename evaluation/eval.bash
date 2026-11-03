python - <<'PY'
import pandas as pd

df = pd.read_csv("evaluation/results/rag_evaluation_results.csv")

answerable = df[df["answerable"] == 1]
valid_retrieval = answerable.dropna(subset=["retrieval_hit"])

successful = df[
    df["error"].fillna("").eq("")
    & df["chat_latency_s"].notna()
]

print("=== RAG EVALUATION SUMMARY ===")
print("Total questions:", len(df))
print("Successful chat requests:", len(successful))
print("Failed requests:", len(df) - len(successful))

if len(valid_retrieval):
    print(
        "Retrieval Hit@4:",
        round(valid_retrieval["retrieval_hit"].mean(), 4)
    )

if len(successful):
    print(
        "Average chat latency:",
        round(successful["chat_latency_s"].mean(), 3),
        "seconds"
    )
PY