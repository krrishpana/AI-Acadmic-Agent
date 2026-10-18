import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))   # so we can import your src/ modules

import query_engine


def check(results, expected_source, expected_pages):
    doc_hit = False
    page_hit = False
    for item in results:
        meta = item["metadata"]
        if meta.get("source") == expected_source:
            doc_hit = True
            if meta.get("page") in expected_pages:
                page_hit = True
    return doc_hit, page_hit


def main(top_k: int = 4):
    cases = json.loads((ROOT / "eval" / "retrieval_set.json").read_text())
    doc_hits = 0
    page_hits = 0

    for case in cases:
        results = query_engine.retrieve(case["question"], top_k)
        doc_hit, page_hit = check(results, case["source"], case["pages"])
        doc_hits += doc_hit
        page_hits += page_hit

        mark = "✅" if page_hit else ("🟡" if doc_hit else "❌")
        print(f"{mark} {case['question']}")
        if not page_hit:
            found = [f"{r['metadata'].get('source')} p{r['metadata'].get('page')}" for r in results]
            print(f"     expected: {case['source']} p{case['pages']}")
            print(f"     got:      {found}")

    n = len(cases)
    print(f"\nRight document in top {top_k}: {doc_hits}/{n} = {doc_hits / n:.0%}")
    print(f"Right page in top {top_k}:     {page_hits}/{n} = {page_hits / n:.0%}")


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    main(k)