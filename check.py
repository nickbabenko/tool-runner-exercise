# Checks for Part 1. Run with: python3 check.py
# You don't need to change this file.

import asyncio
import json
import time

from tool_runner import TOOL_TIMEOUT, run_tools


def call(id, name, arguments):
    return {"id": id, "name": name, "arguments": arguments if isinstance(arguments, str) else json.dumps(arguments)}


def run(calls):
    async def main():
        return await asyncio.wait_for(run_tools(calls), timeout=5)

    started = time.perf_counter()
    try:
        results = asyncio.run(main())
    except asyncio.TimeoutError:
        raise AssertionError("run_tools was still going after 5s")
    return results, time.perf_counter() - started


def check_results_stay_in_call_order():
    results, _ = run([
        call("slow", "search_products", {"query": "vegan"}),
        call("fast", "get_product", {"product_id": "p-101"}),
    ])
    assert isinstance(results, list), f"expected a list, got {results!r}"
    assert [r.get("id") for r in results] == ["slow", "fast"], f"got {results}"
    assert all("result" in r for r in results), f"both calls should have a result: {results}"


def check_one_bad_call_does_not_lose_the_others():
    results, _ = run([
        call("1", "search_products", {"query": "vegan"}),
        call("2", "check_delivery", {"postcode": "M1 1AA"}),
        call("3", "get_product", '{"product_id": "p-102"'),
        call("4", "add_to_basket", {"product_id": "p-103", "quantity": 1}),
        call("5", "get_product", {"sku": "p-101"}),
    ])
    assert isinstance(results, list) and len(results) == 5, f"expected 5 results, got {results!r}"
    assert "result" in results[0], f"call 1 should have a result: {results[0]}"
    for bad in results[1:]:
        assert isinstance(bad.get("error"), str) and bad["error"], f"expected an error message: {bad}"


def check_tools_run_concurrently():
    results, elapsed = run([
        call("1", "search_products", {"query": "vegan"}),
        call("2", "check_stock", {"product_id": "p-101"}),
        call("3", "check_stock", {"product_id": "p-102"}),
    ])
    assert isinstance(results, list) and all("result" in r for r in results), f"got {results!r}"
    assert elapsed < 0.8, f"took {elapsed:.2f}s, should take about 0.5s"


def check_slow_tool_times_out():
    results, elapsed = run([
        call("1", "track_order", {"order_id": "o-123"}),
        call("2", "get_product", {"product_id": "p-101"}),
    ])
    assert isinstance(results, list) and len(results) == 2, f"expected 2 results, got {results!r}"
    assert elapsed < TOOL_TIMEOUT + 0.5, f"took {elapsed:.2f}s, TOOL_TIMEOUT is {TOOL_TIMEOUT}s"
    assert isinstance(results[0].get("error"), str) and results[0]["error"], f"expected an error message: {results[0]}"
    assert "result" in results[1], f"call 2 should have a result: {results[1]}"


def check_results_can_go_back_to_the_model():
    results, _ = run([call("1", "search_products", {"query": "vegan"})])
    assert isinstance(results, list) and results and results[0].get("result"), f"got {results!r}"
    json.dumps(results)


if __name__ == "__main__":
    for check in [
        check_results_stay_in_call_order,
        check_one_bad_call_does_not_lose_the_others,
        check_tools_run_concurrently,
        check_slow_tool_times_out,
        check_results_can_go_back_to_the_model,
    ]:
        try:
            check()
            print(f"PASS  {check.__name__}")
        except Exception as e:
            print(f"FAIL  {check.__name__}: {type(e).__name__}: {e}")
