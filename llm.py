import sys
sys.stdout.reconfigure(encoding='utf-8')

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from config import get_api_key, get_model_name

def chat(messages):
    """
    messages: list of dicts {"role": "...", "content": "..."}
    Returns: str response from LLM
    Client is created at call-time so secrets are always loaded.
    """
    # Client har call pe fresh banao — taaki secrets sahi milein
    client = ChatMistralAI(
        api_key=get_api_key(),
        model=get_model_name()
    )

    lc_messages = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            lc_messages.append(SystemMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessage(content=content))
        else:
            lc_messages.append(HumanMessage(content=content))

    response = client.invoke(lc_messages)
    return response.content

if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "say hello"}
    ]
    print(chat(messages))