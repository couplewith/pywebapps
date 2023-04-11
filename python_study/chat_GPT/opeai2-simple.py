import openai
openai.api_type = "azure"
openai.api_key = "..."
openai.api_base = "https://example-endpoint.openai.azure.com"
openai.api_version = "2022-12-01"

# create a completion
completion = openai.Completion.create(engine="deployment-name", prompt="Hello world")

# print the completion
print(completion.choices[0].text)