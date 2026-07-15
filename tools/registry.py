from .calculator import execute as calculator
from .type_tool import execute as type_tool
from .weather import execute as weather
from .web_search import execute as web_search
from .scrape_url import execute as scrape_url

TOOLS = {
    "calculator": calculator,
    "time": type_tool,
    "weather": weather,
    "web_search": web_search,
    "scrape_url": scrape_url,
}



def execute_tool(tool_name: str, arguments:dict):
    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"unknown tool: {tool_name}"
    return tool(arguments)

def list_tools():
    return list(TOOLS.keys())

if __name__ == "__main__":
    print("Registered tools\n")
    print(
        execute_tool(
            "calculator",
            {"expression": "12+13"}
        )
    )
     
    print("\n")

    print(
        execute_tool(
            "time",
            {}
        )
    )

    print("\n")
    print(
        execute_tool(
            "weather",
            {"city": "kolkata"}
        )
    )