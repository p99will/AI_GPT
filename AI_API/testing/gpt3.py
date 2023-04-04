import openai
import os

# Authenticate with the OpenAI API using your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the initial prompt and parameters for the Completion API request
prompt = ""
params = {
    "model": "gpt-3.5-turbo",
    "prompt": prompt,
    "temperature": 0.5,
    "max_tokens": 200,
}

params["prompt"] = ""
def ask_me(question):
    params["prompt"] += question
    response = openai.ChatCompletion.create(**params)
    generated_text = response.choices[0].text.strip()
    print("ChatBOT: " + generated_text)
    params["prompt"] += "\n" + generated_text + '\n'

while 1:
    prompt = input("> ")
    ask_me(prompt)