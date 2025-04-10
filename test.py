# from huggingface_hub import InferenceClient
# import pyautogui
# import base64
# import pathlib

# client = InferenceClient(
# 	api_key="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"
# )

# im1 = pyautogui.screenshot()
# im1.save(r"C:\Users\2025130\Documents\aiagent\screenshot.jpeg")
# # image_path = pathlib.Path("C:\\Users\\2025130\\Documents\\aiagent\\screenshot.png").as_uri()

# with open(r"C:\Users\2025130\Documents\aiagent\screenshot.jpeg", "rb") as f:
#     image = base64.b64encode(f.read()).decode("utf-8")

# image = f"data:image/jpeg;base64,{image}"
# print("encoded image", image[:100])


# messages = [
# 	{
# 		"role": "user",
# 		"content": [
# 			{
# 				"type": "text",
# 				"text": "Describe this image in one sentence."
# 			},
# 			{
# 				"type": "image_url",
# 				"image_url": {
#                     "url": image
# 					# "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
# 				}
# 			}
# 		]
# 	}
# ]

# stream = client.chat.completions.create(
# 	model="Qwen/Qwen2.5-VL-7B-Instruct", 
# 	messages=messages, 
# 	max_tokens=500,
# 	stream=True
# )

# for chunk in stream:
#     print(chunk.choices[0].delta.content, end="")
