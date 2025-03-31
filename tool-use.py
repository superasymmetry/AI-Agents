import instructor
from pydantic import BaseModel, Field
from groq import Groq
from agents.auto import AutomationAgent

class ToolUseModel():
    def __init__(self):
        
        # Define the tool schemas for Groq, describing each available tool.
        self.tool_schema = {
            "click_at_xy": {
                "name": "cursor_click",
                "description": "Click on a specific clickable feature on the screen.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "integer",
                            "description": "The x coordinate for the click action."
                        },
                        "y": {
                            "type": "integer",
                            "description": "The y coordinate for the click action."
                        }
                    },
                    "required": ["x", "y"]
                }
            },
            "move_cursor": {
                "name": "move_cursor",
                "description": "Move the cursor to a specific coordinate. This is only used when a click in that location is not needed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "integer",
                            "description": "The x coordinate to move the cursor to."
                        },
                        "y": {
                            "type": "integer",
                            "description": "The y coordinate to move the cursor to."
                        }
                    },
                    "required": ["x", "y"]
                }
            },
            "type": {
                "name": "type_text",
                "description": "Type a string of text on the screen.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to type."
                        }
                    },
                    "required": ["text"]
                }
            },
            "scroll": {
                "name": "scroll",
                "description": "Scroll up or down on the screen.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "direction": {
                            "type": "string",
                            "enum": ["up", "down"],
                            "description": "The direction to scroll."
                        },
                        "amount": {
                            "type": "integer",
                            "description": "The amount to scroll."
                        }
                    },
                    "required": ["direction", "amount"]
                }
            },
        }

# Define the Pydantic model for the tool call
class ToolCall(BaseModel):
    input_text: str = Field(description="The user's input text")
    tool_name: str = Field(description="The name of the tool to call")
    tool_parameters: str = Field(description="JSON string of tool parameters")

class ResponseModel(BaseModel):
    tool_calls: list[ToolCall]

# Patch Groq() with instructor
client = instructor.from_groq(Groq(api_key="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"), mode=instructor.Mode.JSON)

def run_conversation(user_prompt, ui_features):
    # Prepare the messages

    messages = [
        {
            "role": "system",
            "content": f"You are an assistant that can use tools. You have access to the following actions/tools: {tool_schema}."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    # Make the Groq API call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=ResponseModel,
        messages=messages,
        temperature=0.2,
        max_tokens=128,
    )

    return response.tool_calls

# Example usage
user_prompt = "Open google chrome and search for the weather in Oakville"
a = AutomationAgent()
tree = a.get_major_controls(a.root_control)
tool_calls = run_conversation(user_prompt, tree)

for call in tool_calls:
    print(f"Input: {call.input_text}")
    print(f"Tool: {call.tool_name}")
    print(f"Parameters: {call.tool_parameters}")
    print()