import uiautomation as automation
import pyautogui
from groq import Groq
import os
import json
import base64

class AutomationAgent():
    def __init__(self):
        # for UIAutomation
        self.max_depth = 6
        self.root_control = automation.GetRootControl()
        # Use a dictionary comprehension to assign a separate list for each key.
        self.tree = {key: [] for key in [
            'WindowControl', 'PaneControl', 'DocumentControl', 'ButtonControl',
            'EditControl', 'CheckBoxControl', 'RadioButtonControl', 'ComboBoxControl',
            'ListControl', 'ListItemControl', 'MenuControl', 'TreeControl',
            'TabControl', 'SliderControl', 'CustomControl'
        ]}

        # for Groq client
        self.action_history = []
        self.task = ""
        basedir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(basedir, 'config.json')
        with open(folder_path, "rb") as config_file:
            config = json.load(config_file)
        self.api_key = config["api_key"]
        self.client = Groq(api_key=self.api_key)
        
        self.task_library = {
            "click_at_xy": self.click,
            "move_cursor": self.move_cursor,
            "type": self.type,
            "select": self.select,
            "scroll": self.scroll,
            # "search_web": self.search_web,
        }

        with open("prompt.md", "r", encoding="utf-8") as file:
            self.prompt_template = file.read()

    def get_control_coordinates(self, control):
        """Return control's bounding rectangle as (left, top, width, height) if available."""
        try:
            rect = control.BoundingRectangle
            if isinstance(rect, tuple) and len(rect) == 4:
                left, top, right, bottom = rect
            else:
                left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
            width = right - left
            height = bottom - top
            return (left, top, width, height)
        except Exception as e:
            print(f"Error getting coordinates for {control.ControlTypeName}: {e}")
            return None

    def get_major_controls(self, control, indent=0, max_depth=None):
        if max_depth is None:
            max_depth = self.max_depth
        if indent // 4 >= max_depth:
            return

        try:
            # Skip controls that are offscreen
            if control.IsOffscreen:
                return

            # Process the current control
            name = control.Name.strip() if control.Name else ''
            coords = self.get_control_coordinates(control)
            if name and coords:
                controlType = control.ControlTypeName
                # Only add if the controlType is one of the keys in our tree.
                if controlType in self.tree:
                    self.tree[controlType].append({"feature": name, "coordinates": coords})
                    print(f"Added {controlType}: {name} - Coordinates: {coords}")
        except Exception as e:
            try:
                ctype = control.ControlTypeName
            except Exception:
                ctype = "<unknown>"
            print(' ' * indent + f'{ctype}: <error retrieving info> - {e}')

        try:
            # Recursively process child controls
            for child in control.GetChildren():
                self.get_major_controls(child, indent + 4, max_depth)
        except Exception as e:
            print(' ' * indent + f'<error iterating children> - {e}')

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
    
    def search_web(self, query):
        pass
    
    def get_action(self, task, tree):
        # Format the system message with the prompt
        system_message = self.prompt_template

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": f"{system_message} given that the UI features are: {tree}",
                },
                {
                    "role": "user",
                    "content": task
                }
            ],

        )
        return completion.choices[0].message.content
    
    def getTree(self):
        return self.tree
    
    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        basedir = os.path.dirname(os.path.abspath(__file__))
        file_dir = os.path.join(basedir, "files")
        screenshot.save(os.path.join(file_dir,"screenshot.png"))
        image_path = file_dir+"/screenshot.png"
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

if __name__ == "__main__":
    agent = AutomationAgent()
    # Start recursion with the root control
    agent.get_major_controls(agent.root_control)
    tree = agent.getTree()
    print(tree)
    msg = input("Query: ")
    print(agent.get_action(msg, tree))
