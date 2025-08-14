from typing import List, Any

def print_state_messages(stream: List[dict[str, Any]]) -> None:
    """Prints each message from the stream in a readable format."""
    for s in stream:
        messages = s.get("messages", [])
        if not messages:
            print("No messages to display.")
            continue
        message = messages[-1]
        if hasattr(message, "pretty_print") and callable(message.pretty_print):
            message.pretty_print()
        else:
            print(str(message))