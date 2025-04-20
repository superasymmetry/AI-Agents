from openai import OpenAI
import pyautogui
import base64

class agenticModel():
    def __init__(self):
        self.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
        )

    def capture_screen(self):
        im1 = pyautogui.screenshot()
        im1.save(r"C:\Users\2025130\Documents\aiagent\screenshot.jpeg")
        # image_path = pathlib.Path("C:\\Users\\2025130\\Documents\\aiagent\\screenshot.png").as_uri()

        with open(r"C:\Users\2025130\Documents\aiagent\screenshot.jpeg", "rb") as f:
            img = base64.b64encode(f.read()).decode("utf-8")

        img = f"data:image/jpeg;base64,{img}"
        return img

    def call(self, query, img_base64, chat_history):
        completion = self.client.chat.completions.create(
        model="qwen/qwen2.5-vl-32b-instruct:free",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f'You are an agent that navigates the laptop and executes tasks. The user originally wants you to "{query}". You already attempted to perform these actions {chat_history}. However, observe the screenshot and understand what the screen is currently on to determine whether or not your actions have been correcly performed (if not, find a way to correctly do the action again). Decompose the user\'s query into its most fundamental steps, which must be one of left-clicking, right-clicking, typing, dragging the cursor, scrolling, or pressing hotkeys. Think step-by-step the entire rest of the process of executing the task to determine the immediate next action to perform based on the given screen. Please output **one sentence** that states the immediate next step AND ONLY THE IMMEDIATE NEXT STEP NOTHING MORE to performing the user\'s query. Be very clear but concise in your description of the immediate next step so that there are no ambiguities. If you realize the task is already finished, output "Task completed".'
                # "text": prompt.format(query=query, chat_history=chat_history),
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": img_base64
                }
                }
            ]
            }
        ]
        )
        return (completion.choices[0].message.content)
    
if __name__ == "__main__":
    agentic_model = agenticModel()
    screenshot_base64 = agentic_model.capture_screen()
    response = agentic_model.call("Open Google Chrome and search for the weather", screenshot_base64, [])
    print(response)