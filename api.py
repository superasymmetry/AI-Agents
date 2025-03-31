import uiautomation as auto
from groq import Groq
import json
import os
import pyautogui

class agent():
    def __init__(self):
        self.action_history = []
        self.task = ""
        basedir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(basedir,'config.json')
        with open((folder_path), "rb") as config_file:
            config = json.load(config_file)
        self.api_key = config["api_key"]
        self.client = Groq(
            api_key = self.api_key,
        )
        self.ROUTING_MODEL = "llama3-70b-8192"
        self.TOOL_USE_MODEL = "llama-3.3-70b-versatile"
        self.GENERAL_MODEL = "llama3-70b-8192"
        
        self.task_library = {
            "click_at_xy": self.click,
            "move_cursor": self.move_cursor,
            "type": self.type,
            "select": self.select,
            "scroll": self.scroll,
        }

    def move_cursor(self, x, y):
        pyautogui.moveTo(x, y)
        return True
    
    def click(self, x, y):
        pyautogui.click(x, y)
        return True
    
    def type(self, text):
        pyautogui.typewrite(text)
        return True

    def select(self, text):
        pyautogui.press('down')
        
    def scroll(self, direction):
        if direction == "up":
            pyautogui.scroll(1)
        elif direction == "down":
            pyautogui.scroll(-1)

    def get_action(self, task):
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant operating this computer."
                },
                {
                    "role": "user",
                    "content": f"{task}"
                }
            ]
        )
        return (completion.choices[0].message.content)
    
    def get_ui_tree(self):
        root = auto.GetRootControl()
        elements = []

        def traverse(control):
            for child in control.GetChildren():
                elements.append({
                    "name": child.Name,
                    "role": child.ControlTypeName,
                    "bounds": child.BoundingRectangle
                })
                print(elements)
                traverse(child)

        traverse(root)
        return elements
    
    def execute_task(self, task):
        if task in self.task_library:
            self.task_library[task]()
            return True
        else:
            return False

a = agent()
print(a.get_ui_tree())