# Retrieval Benchmark v1

## Environment

- Embedding model: `nomic-embed-text`
- Vector database: Qdrant local
- LLM: `qwen2.5:0.5b`
- Dataset: MSc course material
- Evaluation questions: 7 in-domain questions

## Results

| Metric | Result |
|---|---:|
| Recall@1 | 100% (7/7) |
| Recall@3 | 100% (7/7) |
| Recall@5 | 100% (7/7) |

## Queries

| ID | Question | Expected slide(s) | Top-1 |
|---|---|---|---:|
| q01 | What is Big Data? | 9 | 9 |
| q02 | What are the waves of managing data? | 2, 3, 5, 6, 8 | 2 |
| q03 | What is Volume in Big Data? | 13 | 13 |
| q04 | What is Velocity in Big Data? | 14 | 14 |
| q05 | What is Variety in Big Data? | 15 | 15 |
| q06 | What is Veracity in Big Data? | 16 | 16 |
| q10 | What is a relational database? | 3, 4, 67 | 67 |

## Interpretation

All 7 in-domain evaluation queries retrieved at least one
expected relevant slide in the top 1, top 3, and top 5 results.

This is an initial benchmark only and should not be interpreted
as general retrieval accuracy. The evaluation dataset is small
and manually constructed.