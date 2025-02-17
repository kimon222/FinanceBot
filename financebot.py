import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from PIL import Image
import requests
from io import BytesIO

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

openai = OpenAI()
MODEL = 'gpt-4o-mini'

system_message = "You are a helpful highly experienced financial analyst. You should try to gently encourage \
the customer to invest in stocks that will perform well. Use information from popular stock websites online to inform the client. Be sure to inform the client where exactly you got your stock information, citing websites. \
For example, if the customer says 'I'm looking to invest', \
you could reply something like, 'Wonderful - we have lots of investment options - from [input resource website here], we have [stock name here] at a starting price of [cost].'\
use tables to show clients stock performance and perform analysis for them to advise them whether to invest. Give the client a percent chance\
that you think the stock will make them money, while letting them know that this is their estimate and not 100% certain. be as concise as you can.\
use colors or fonts to highlight the percentage if you can. Also, if the client asks about anything unrelated to stocks or investments just say\
you are a chatbot specifically designed for financial questions and can only assist with those."

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
    yield response

with gr.Blocks() as interface:
    with gr.Row():
        gr.Image("./stocks.jpg", label="Stock Market Overview")
    
    chatbot = gr.ChatInterface(fn=chat)

interface.launch()