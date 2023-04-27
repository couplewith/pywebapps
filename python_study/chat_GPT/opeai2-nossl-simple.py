import openai
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set up OpenAI API credentials
#openai.api_key = "YOUR_API_KEY"
openai.api_key = "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"

# create a completion without SSL verification
completion = openai.Completion.create(
    engine="davinci",
    prompt="Hello world",
    max_tokens=5,
    n=1,
    stop=None,
    temperature=0.5,
    timeout=10,
    verify=False
)

# print the completion
print(completion.choices[0].text)
