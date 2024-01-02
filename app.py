# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: title,-all
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
import time

import google.generativeai as genai
import gradio as gr
import PIL.Image
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.schema import ImageDocument

# %% [markdown]
# # Setup and configuration

# %% Configuration
GOOGLE_API_KEY='AIzaSyDP9Wv8Q-2vRJFQge-zyO138qdokEUMe3k'  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# %% [markdown]
# # Functions

# %%
all_image_documents = []

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)
    
def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def store_image(history):
    # Get the uploaded file
    image_path = history[0][0][0]
    print(image_path)
    all_image_documents.append(ImageDocument(image_path=image_path))

    status = "Uploaded successfuly"

    history[-1][1] = ""
    for character in status:
        history[-1][1] += character
        time.sleep(0.01)
        yield history


def bot_text(history):
    
    prompt = history[-1][0]
    
    # Process with Gemini pro-vision
    gemini_pro = GeminiMultiModal(model_name="models/gemini-pro-vision")
    complete_response = gemini_pro.complete(
        prompt=prompt,
        image_documents=all_image_documents,
    )

    history[-1][1] = ""
    # print(f"complete_response {complete_response}-{type(complete_response)}")
    for character in complete_response.text:
        history[-1][1] += character
        time.sleep(0.05)
        yield history





# %% [markdown]
# # Gradio main block

# %%
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    # Submit text
    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot_text, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)

    # Upload picture
    # file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
    #     bot_picture, chatbot, chatbot
    # )
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        store_image, chatbot, chatbot
    )

    chatbot.like(print_like_dislike, None, None)



demo.queue()
demo.launch()

