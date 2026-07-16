import sys
sys.stdout.reconfigure(encoding='utf-8')

from AgentTool import Agent
import json

agent = Agent()
user_input = "6-2"

print("--- Testing '6-2' ---")
# Let's run steps of Agent manually to see what's happening
from llm import chat
from memory import load_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_calls

memory = load_memory()
messages = [{"role": "system", "content": SYSTEM_PROMPT}]
messages.extend(memory)
messages.append({"role": "user", "content": user_input})

print("LLM Input messages:")
for m in messages[-2:]:
    print(f"Role: {m['role']} | Content: {m['content']}")

llm_response = chat(messages)
print(f"\nLLM Initial Response:\n{llm_response}")

tool_requests = parse_tool_calls(llm_response)
print(f"\nParsed Tool Requests: {tool_requests}")

from AgentTool import llm_refused_tool, detect_forced_tool
refused = llm_refused_tool(llm_response)
print(f"LLM Refused Tool: {refused}")
if not tool_requests and refused:
    forced = detect_forced_tool(user_input)
    print(f"Forced Tool: {forced}")
