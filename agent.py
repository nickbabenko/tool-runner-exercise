# Part 2: code review.
#
# A teammate has opened a PR adding this shopping assistant agent loop.
# call_model (model.py) is a mock LLM with tool calling. The tools are in tools.py.
# Run it with: python3 shop.py
#
# Review it as you would a real PR: what would you comment on, and what would you change?

import json

from model import call_model
from tools import add_to_basket, search_products

TOOLS = {
    "search_products": search_products,
    "add_to_basket": add_to_basket,
}


async def run_agent(user_message, messages=[]):
    messages.append({"role": "user", "content": user_message})

    while True:
        response = await call_model(messages)

        if response["type"] == "final":
            messages.append({"role": "assistant", "content": response["text"]})
            return response["text"]

        tool_call = response["tool_call"]
        messages.append({"role": "assistant", "tool_call": tool_call})

        result = await TOOLS[tool_call["name"]](**json.loads(tool_call["arguments"]))
        messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(result, default=str)})
