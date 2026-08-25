import json
from pathlib import Path
from llm import get_response

def load_test_cases(path="test_cases.json"):
    test_cases_path = Path(path)
    if not test_cases_path.is_absolute():
        test_cases_path = Path(__file__).resolve().parent / test_cases_path

    with test_cases_path.open() as f:
        return json.load(f)

def run_case(case):
    try:
        result = get_response(case["query"], case["session_id"])
    except Exception as e:
        return {
            "id": case["id"],
            "passed": False,
            "reasons": [str(e)],
            "actual_answer": None
        }

    passed = True
    reasons = []
    expected = case["expected"]

    if "tool_called" in expected:
        actual_tool = getattr(result.metadata, "tool_used", None)

        if expected["tool_called"] and expected["tool_called"] != actual_tool:
            passed = False
            reasons.append(f"Expected tool '{expected['tool_called']}', but got '{actual_tool}'")

        if not expected["tool_called"] and actual_tool:
            passed = False
            reasons.append(f"Unexpected tool '{actual_tool}' called")

    if "answer_contains" in expected:
        if expected["answer_contains"].lower() not in result.short_answer.lower():
            passed = False
            reasons.append(f"expected {expected["answer_contains"]} in answer")

    if "answer_not_contains" in expected:
        if expected["answer_not_contains"].lower() in result.short_answer.lower():
            passed = False
            reasons.append(f"expected {expected["answer_not_contains"]} to not be in answer")

    return {
        "id": case["id"],
        "passed": passed,
        "reasons": reasons,
        "actual_answer" : result.short_answer
    }

def run_all():
    test_cases = load_test_cases()
    results = [run_case(c) for c in test_cases]

    passed = sum(result["passed"] for result in results)
    print(f"{passed}/{len(results)} passed\n")

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['id']}")
        if not r["passed"]:
            print(f"  reasons: {r['reasons']}")
            print(f"  actual: {r['actual_answer']}")

if __name__ == "__main__":
    run_all()