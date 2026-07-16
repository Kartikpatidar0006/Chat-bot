import os
import json

MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.json")


MAX_MEMORY_PAIRS = 10 

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            memory = json.load(file)
            
            max_msgs = MAX_MEMORY_PAIRS * 2
            return memory[-max_msgs:] if len(memory) > max_msgs else memory
    except Exception:
        return []


def save_memory(memory):
   
    max_msgs = MAX_MEMORY_PAIRS * 2
    if len(memory) > max_msgs:
        memory = memory[-max_msgs:]
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, ensure_ascii=False, indent=4)


def add_message(memory, role, content):
    memory.append({
        "role": role,
        "content": content
    })
    return memory


if __name__ == "__main__":
    print("Loading memory...")
    memory = load_memory()

    print(memory)

    print("\nAdding Message to memory...")

    add_message(memory, "user", "Hello, how are you?")
    add_message(memory, "assistant", "I'm doing well, thank you!")

    save_memory(memory)

    print(load_memory())