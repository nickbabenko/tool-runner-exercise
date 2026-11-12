# Mock LLM. You don't need to change this file.
# Behaves like a chat model with tool calling. Responses take 0.2-0.6s.
#
# call_model(messages) returns one of:
#   {"type": "tool_call", "tool_call": {"id": ..., "name": ..., "arguments": "<JSON string>"}}
#   {"type": "final", "text": ...}

import asyncio
import json
import random


def _tool_call(id, name, args):
    print(f"  [model] {name}({json.dumps(args)})  id={id}")
    return {"type": "tool_call", "tool_call": {"id": id, "name": name, "arguments": json.dumps(args)}}


def _final(text):
    print("  [model] final answer")
    return {"type": "final", "text": text}


async def call_model(messages):
    await asyncio.sleep(0.2 + random.random() * 0.4)

    first = next((m for m in messages if m["role"] == "user"), None)
    prompt = first["content"].lower() if first else ""
    n = sum(1 for m in messages if m["role"] == "tool")

    if "compare" in prompt:
        return _tool_call(f"call_{n}", "search_products", {"query": f"protein {n}"})

    if "deliver" in prompt:
        if n == 0:
            return _tool_call("call_0", "check_delivery", {"postcode": "M1 1AA"})
        return _final("Good news, it'll be with you by Friday.")

    if n == 0:
        return _tool_call("call_0", "search_products", {"query": "vegan protein", "max_price": 30})
    if n == 1:
        return _tool_call("call_1", "add_to_basket", {"product_id": "p-102", "quantity": 2})
    if n == 2:
        return _tool_call("call_1", "add_to_basket", {"product_id": "p-102", "quantity": 2})
    return _final("I've added 2 x Vegan Protein Powder (Chocolate) to your basket.")
