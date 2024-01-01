# -*- coding: utf-8 -*-
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

# %%
import os
import time

# %%
import google.generativeai as genai
import gradio as gr
import PIL.Image

# %%
# Configure Gemini Pro Vision
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro-vision')

path_temp = ""

# %%
# Function to generate content using Gemini Pro Vision
def generate_content(history, prompt, file_path):
    img = PIL.Image.open(file_path)
    response = model.generate_content([prompt, img])
    generated_text = response.text

    # Update the chat history with the generated text
    history[-1][1] = generated_text

    return history

# %%
# Gradio code
def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

# %%
def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)
    


# %%
def add_file(history, file):
    history = history + [((file.name,), None)]
    return history



# %%
def bot_text(history):
    response = "**That's cool!**"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

def bot_picture(history):
    history[-1][1] = ""
    for character in history[0][0]:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

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

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot_text, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot_picture, chatbot, chatbot
    )

    chatbot.like(print_like_dislike, None, None)




demo.queue()
demo.launch()

