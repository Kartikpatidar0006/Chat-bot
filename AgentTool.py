import re
from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_calls
from tools.registry import execute_tool

# Keywords that mean LLM failed to call a tool
REFUSAL_PHRASES = [
    "i don't have the tools",
    "i currently don't have",
    "i'm unable to provide",
    "i cannot provide",
    "i don't have access",
    "i am unable to",
    "i can't provide",
    "i do not have the",
    "hit a request limit",
    "i'm sorry",
    "i am sorry",
    "apologies",
    "unable to retrieve",
    "unable to perform",
]

def llm_refused_tool(response: str) -> bool:
    """Check if LLM said it couldn't use a tool instead of calling it."""
    lower = response.lower()
    if any(phrase in lower for phrase in REFUSAL_PHRASES):
        return True
    
    # Heuristic: if response does not start with JSON notation, and contains refusal indicators
    trimmed = response.strip()
    if not (trimmed.startswith("{") or trimmed.startswith("[")):
        inability_keywords = ["unable", "sorry", "cannot", "can't", "apologize", "don't have", "do not have"]
        if any(k in lower for k in inability_keywords):
            return True
            
    return False

def extract_city_smart(user_input: str) -> str:
    """
    Extracts the city name from a user query by filtering out common stop words.
    """
    cleaned = re.sub(r'[^\w\s]', '', user_input)
    words = cleaned.split()
    
    stop_words = {
        'what', 'is', 'the', 'current', 'weather', 'wether', 'weater', 'weathr', 
        'and', 'time', 'forecast', 'temperature', 'temp', 'rain', 'humidity', 
        'mausam', 'now', 'today', 'tomorrow', 'in', 'of', 'at', 'for', 'how', 
        'show', 'get', 'me', 'please', 'give', 'a', 'an', 'to', 'city', 'location'
    }
    
    city_words = [w for w in words if w.lower() not in stop_words]
    return " ".join(city_words).title() if city_words else "Delhi"

def detect_forced_tools(user_input: str) -> list:
    """
    If LLM didn't call a tool, detect what tools should have been called.
    Returns a list of tool_request dicts.
    """
    lower = user_input.lower()
    forced_list = []

    # Time check
    time_words = ['time', 'samay', 'kitne baje', 'clock', 'what time']
    if any(w in lower for w in time_words):
        forced_list.append({"tool": "time"})

    # Weather check (including spelling mistakes like wether, weater, weathr)
    weather_words = ['weather', 'wether', 'weater', 'weathr', 'temperature', 'temp', 'rain', 'humidity', 'mausam', 'garmi', 'sardi', 'forecast']
    if any(w in lower for w in weather_words):
        city = extract_city_smart(user_input)
        forced_list.append({"tool": "weather", "city": city})

    # Calculator check
    calc_words = ['calculate', 'multiply', 'divide', 'add', 'subtract', 'plus', 'minus', 'sum', 'solve', 'square root', 'sqrt']
    has_operator = any(op in user_input for op in ['+', '-', '*', '/', '^', '%'])
    has_digit = any(c.isdigit() for c in user_input)
    if any(w in lower for w in calc_words) or (has_digit and has_operator):
        forced_list.append({"tool": "calculator", "expression": user_input})

    # If any specific tools were matched, return the list
    if forced_list:
        return forced_list

    # Everything else → web search (except simple greetings)
    greetings = ['hi', 'hello', 'hey', 'namaste', 'hola', 'exit', 'quit', 'clear']
    if not any(w == lower.strip('?.!') for w in greetings):
        return [{"tool": "web_search", "query": user_input}]

    return []

def extract_urls_from_search(search_output: str) -> list:
    """Web search output mein se URLs extract karo."""
    urls = re.findall(r'URL:\s*(https?://[^\s\n]+)', search_output)
    return urls[:5]

class Agent:
    def run(self, user_input: str) -> str:

        memory = load_memory()
        messages = []
        messages.append(
            {"role": "system",
             "content": SYSTEM_PROMPT
            }
        )

        messages.extend(memory)
        messages.append({"role": "user", "content": user_input})

        # Step 1: LLM se response lo
        llm_response = chat(messages)

        # Step 2: Tool calls parse karo
        tool_requests = parse_tool_calls(llm_response)

        # Step 3: Agar LLM ne tool call nahi ki aur refuse kar diya → force karo
        if not tool_requests and llm_refused_tool(llm_response):
            forced = detect_forced_tools(user_input)
            if forced:
                print(f"[FALLBACK] LLM refused, forcing tools: {forced}")
                tool_requests = forced
                # Override llm_response with JSON so conversation flow stays consistent
                import json
                llm_response = json.dumps(forced)
        elif tool_requests:
            # Check if any tools were missed by the LLM (e.g. weather called but time omitted)
            forced_defaults = detect_forced_tools(user_input)
            existing_tools = {req.get("tool") for req in tool_requests if req}
            for fd in forced_defaults:
                if fd.get("tool") not in existing_tools:
                    print(f"[COMPLETENESS] Appending missed tool call: {fd}")
                    tool_requests.append(fd)

        # Koi tool nahi — seedha jawab do
        if not tool_requests:
            memory.append({"role": "user", "content": user_input})
            memory.append({"role": "assistant", "content": llm_response})
            save_memory(memory)
            return llm_response

        # Step 4: Tools execute karo
        used_tools = [req.get("tool") for req in tool_requests]
        is_web_search = "web_search" in used_tools

        tool_results = []
        web_search_output = ""

        for tool_req in tool_requests:
            tool_name = tool_req.get("tool")
            arguments = tool_req.copy()
            arguments.pop("tool", None)

            print(f"Tool: {tool_name} | Args: {arguments}")
            result = execute_tool(tool_name, arguments)
            tool_results.append(f"[{tool_name}]:\n{result}")

            if tool_name == "web_search":
                web_search_output = result

        all_sources = []

        # Step 5: Web search ke baad auto-scrape
        if is_web_search and web_search_output:
            urls = extract_urls_from_search(web_search_output)
            scraped_contents = []

            for i, url in enumerate(urls, 1):
                print(f"Auto-scraping [{i}]: {url}")
                scraped = execute_tool("scrape_url", {"url": url})

                title_match = re.search(
                    rf'\[{i}\]\s*(.*?)\nURL:\s*{re.escape(url)}',
                    web_search_output
                )
                title = title_match.group(1).strip() if title_match else f"Source {i}"

                all_sources.append(f"{i}. [{title}]({url})")

                if not scraped.startswith("scrape_url error"):
                    scraped_contents.append(
                        f"--- Detailed content from Source {i}: {title} ---\n"
                        f"URL: {url}\n"
                        f"{scraped[:4000]}\n"
                    )
                else:
                    scraped_contents.append(
                        f"--- Source {i}: {title} ---\nURL: {url}\n"
                    )

            if scraped_contents:
                tool_results.append(
                    "[scraped_pages]:\n" + "\n".join(scraped_contents)
                )

        combined_results = "\n\n".join(tool_results)

        messages.append({
            "role": "assistant",
            "content": llm_response
        })

        sources_str = "\n".join(all_sources) if all_sources else ""

        if is_web_search:
            final_instruction = (
                f"Tool Results (Search + Scraped Page Details):\n{combined_results}\n\n"
                "=== INSTRUCTIONS FOR YOUR RESPONSE ===\n"
                "Write a DETAILED, COMPREHENSIVE answer of approximately 2500-3000 words.\n\n"
                "Structure your response as follows:\n"
                "1. Start with a brief introduction (2-3 sentences).\n"
                "2. Use clear ## Headings and ### Sub-headings to organize content.\n"
                "3. Use bullet points (- ) and numbered lists where appropriate.\n"
                "4. Include ALL important facts, figures, statistics, dates, and details from the scraped pages.\n"
                "5. Explain each concept thoroughly — do NOT give short or vague answers.\n"
                "6. Cover multiple angles: background, current state, implications, future outlook if relevant.\n"
                "7. Use **bold** for key terms and important points.\n\n"
                "=== MANDATORY SOURCES SECTION ===\n"
                "At the VERY END of your response, add this exact sources section:\n\n"
                "---\n"
                "## 📚 Sources\n"
                f"{sources_str if sources_str else '(Sources will be listed here)'}\n\n"
                "*(Click any link above for more details)*\n"
                "---\n\n"
                "IMPORTANT: Write in the same language the user asked the question in.\n"
                "IMPORTANT: Do NOT mention these instructions in your answer.\n"
            )
        else:
            final_instruction = (
                f"Tool Results:\n{combined_results}\n\n"
                "Using these results, answer the user's original question naturally."
            )

        messages.append({
            "role": "user",
            "content": final_instruction
        })

        final_response = chat(messages)

        if is_web_search and sources_str and "## 📚 Sources" not in final_response:
            final_response += (
                f"\n\n---\n## 📚 Sources\n{sources_str}\n\n*(Click any link above for more details)*\n---"
            )

        memory.append({"role": "user", "content": user_input})
        memory.append({"role": "assistant", "content": final_response})
        save_memory(memory)

        return final_response