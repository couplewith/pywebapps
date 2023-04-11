
import openai
import requests

import openai

#openai.organization = "org-BRTbkUgOGRGwgGz1gjHfpv1X"
#openai.Model.list()

# openai.api_key = "YOUR_API_KEY"
openai.api_key = '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'

#openai.api_base = "https://api.eu-gb.language.ai"
#openai.api_base = "https://api.us-west-2.openai.com"
#openai.api_base = "https://api.openai.com"
#openai.api_base = "https://api.eu-gb.language.ai"

model = "text-davinci-003"
prompt = "Write a short story about a robot"

try:
    response = openai.Completion.create(
      engine=model,
      prompt= prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
      verify=False,
    )
    print(response.choices[0].text)

except openai.error.AuthenticationError as e:
    print("Authentication error: %s" % str(e))
except openai.error.APIConnectionError as e:
    print("Connection error: %s" % str(e))
except openai.error.InvalidRequestError as e:
    print("Invalid request error: %s" % str(e))
except openai.error.OpenAIError as e:
    print("OpenAI API error: %s" % str(e))
except requests.exceptions.RequestException as e:
    print("Request error: %s" % str(e))
