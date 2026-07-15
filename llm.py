# from langchain_mistralai import ChatMistralAI
# from config import API_KEY, MODEL_NAME

# client = ChatMistralAI(
#     api_key=API_KEY,
#     model_name=MODEL_NAME
# )


# def chat(message: list) -> str:
#     response = client.chat.completions.create(
#         messages=message,
#         model=MODEL_NAME,
#         temperature=0
#     )
#     return response.choices[0].message.content.strip()

# if __name__ == "__main__":
#     messages = [
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
#     response = chat(messages)
#     print(response)


import sys
sys.stdout.reconfigure(encoding='utf-8')

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from config import API_KEY, MODEL_NAME

client = ChatMistralAI(
    api_key=API_KEY,
    model=MODEL_NAME
)

def chat(messages):
    """
    messages: list of dicts {"role": "...", "content": "..."}
    Returns: str response from LLM
    """
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
        {"role": "user", "content": "tell me current time and date in india"}
    ]
    print(chat(messages))