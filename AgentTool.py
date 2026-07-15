import re
from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from parser import parse_tool_calls
from tools.registry import execute_tool

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

        llm_response = chat(messages)

        tool_requests = parse_tool_calls(llm_response)

        if not tool_requests:
            memory.append({"role": "user", "content": user_input})
            memory.append({"role": "assistant", "content": llm_response})
            save_memory(memory)
            return llm_response

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
                        f"--- Source {i}: {title} (scraped failed, using search snippet) ---\n"
                        f"URL: {url}\n"
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