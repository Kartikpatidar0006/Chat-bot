import json
import re

def parse_tool_call(response: str):
    try: 
        tool_request = json.loads(response)
        if not isinstance(tool_request, dict):
            return None
        if "tool" not in tool_request:
            return None
        if not isinstance(tool_request["tool"], str):
            return None
        return tool_request
            
    except json.JSONDecodeError:
        return None
    except Exception:
        pass

    return None

def parse_tool_calls(response: str):
    
    results = []

    pattern = r'\{[^{}]+\}'
    matches = re.findall(pattern, response, re.DOTALL)
    for match in matches:
        try:
            obj = json.loads(match)
            if (
                isinstance(obj, dict) and
                "tool" in obj and
                isinstance(obj["tool"], str)
            ):
                results.append(obj)
        except Exception:
            pass
    return results


if __name__ == "__main__":

    response = "Hello, how are you?"
    
    result = parse_tool_call(response)
    print(result)