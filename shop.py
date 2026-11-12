# Part 2: runs the agent in agent.py. You don't need to change this file.
# Each choice is a different shopper sending a message. Ctrl+C stops a run.

import asyncio

from agent import run_agent
from tools import get_basket

MESSAGES = {
    "1": "Add two tubs of vegan chocolate protein to my basket",
    "2": "Compare all your protein products for me",
    "3": "Will it be delivered by Friday? My postcode is M1 1AA",
}


def main():
    while True:
        print()
        for key, message in MESSAGES.items():
            print(f"  {key}  {message}")
        print("  b  Show the basket")
        print("  q  Quit")
        choice = input("> ").strip().lower()

        if choice == "q":
            return
        if choice == "b":
            print(f"Basket: {get_basket()}")
            continue
        if choice not in MESSAGES:
            continue

        print(f"\nShopper: {MESSAGES[choice]}")
        try:
            answer = asyncio.run(run_agent(MESSAGES[choice]))
            print(f"Assistant: {answer}")
        except KeyboardInterrupt:
            print("\nStopped.")
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
        print(f"Basket: {get_basket()}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
