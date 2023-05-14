# -*- coding: utf-8 -*-


import requests
import config


url = "https://openai-api.gpt.jingsan.wang/v1/chat/completions"
api_key = config.openai_api_key
# The headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def chatGpt(prompt):
    # prompt = "translate this sentence to Chinese:Hello world!"
    data = {
        "model":"gpt-3.5-turbo",
        "messages":[{"role":"user","content":prompt}],
        # "max_tokens":800,
        "temperature":0.5,
        "frequency_penalty":0,
        "presence_penalty":0
    }
    # Make the API request
    response = requests.post(url, headers=headers, json=data)
    return eval(response.text)


