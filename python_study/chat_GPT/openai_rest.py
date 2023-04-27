
import requests
import urllib3
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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"
}

data = {
    "prompt": "Hello world",
    "model": "text-davinci-002"
}

response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data, verify=False)

print(response.json()["choices"][0]["text"])