# Part 1: write run_tools.
#
# When the model replies, it can ask for several tools in one go. Each call looks like:
#
#     {"id": "call_1", "name": "search_products", "arguments": '{"query": "vegan protein"}'}
#
# `arguments` is a JSON string, exactly as the model sent it. The tools are in tools.py.
#
# Task: write run_tools(calls). It should:
#   - run the calls at the same time, not one after another
#   - return one result per call, in the same order as `calls`, each either
#         {"id": "call_1", "result": <what the tool returned>}
#     or  {"id": "call_1", "error": "<a message the model can read>"}
#   - not let one bad call lose the others. An unknown tool, bad arguments, a tool that raises,
#     or a tool that takes longer than TOOL_TIMEOUT seconds should each become an error result
#   - return something json.dumps() can handle, because it goes straight back to the model
#
# Check your work with: python3 check.py

from tools import TOOLS

TOOL_TIMEOUT = 1.0  # seconds


async def run_tools(calls):
    # TODO
    pass
