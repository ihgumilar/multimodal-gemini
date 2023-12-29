# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: gemini
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Libraries

# %%
import os
import google.generativeai as genai


# %% [markdown]
# # Setup API

# %%
# Fetch Google API Key from local environment variable
GOOGLE_API_KEY='xxx'
genai.configure(api_key=GOOGLE_API_KEY)

# %% [markdown]
# # List models

# %%
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


# %% [markdown]
# # Define google cloud project information

# %%
# Define project information
import sys

PROJECT_ID = "my-project-indo-409212"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}


# %% [markdown]
# # Chat with video

# %%
import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview import generative_models

vertexai.init(project=PROJECT_ID)



def generate(video):
  model = GenerativeModel("gemini-pro-vision")
  responses = model.generate_content(
    [video, """I want to know more about research method that the speaker talked about in the video"""],
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32
    },
  stream=True,
  )
  
  for response in responses:
      print(response.candidates[0].content.parts[0].text)

video_path='/home/igum002/codes/multimodal-gemini/My_vid_compressed.mp4'
with open(video_path, "rb") as video_file:
  video_bytes = video_file.read()

video = Part.from_data(data=base64.b64encode(video_bytes).decode("utf-8"), mime_type="video/mp4")



# video = Part.from_data(data=base64.b64decode(video_path), mime_type="video/mp4")



# %%
generate(video)

# %%
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel

gemini_pro_vision_model = GenerativeModel("gemini-pro-vision")
response = gemini_pro_vision_model.generate_content([
  "What is in the video? ",
  generative_models.Part.from_data(video_path, mime_type="video/mp4"),
], stream=True)

for chunk in response :
  print(chunk.text)


# %%
# Gemini text
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("What is the meaning of life?")

print(response.text)

# %%
# Gemini pro vision
import google.generativeai as genai
import PIL.Image

img = PIL.Image.open('image_food.png')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')

response = model.generate_content(["Please write copywriting that is concise and meant for customers who mostly work in the Auckland CBD office and have no time to make a lunch", img])

print(response.text)

# %%
# Chat with gemini
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat()

while True:
    message = input("You: ")
    response = chat.send_message(message)

    print("Gemini: " + response.text)

# %%
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel

gemini_pro_vision_model = GenerativeModel("gemini-pro-vision")
response = gemini_pro_vision_model.generate_content([
  "Tell me the objective of the research as discussed in the video? ",
  generative_models.Part.from_uri("https://drive.google.com/file/d/1wCWeGPhvOIkWxFAGlHvbA-Dn5Yq45B2e/view?usp=sharing", mime_type="video/mp4"),
], stream=True)

for chunk in response :
  print(chunk.text)

