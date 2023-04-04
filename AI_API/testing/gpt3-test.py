import openai
import json,os 

openai.api_key = os.getenv("OPENAI_API_KEY")
chat_log = []
def get_response(prompt, chat_log=None):
    if chat_log is None:
        chat_log = []
    prompt = f"{'. '.join(chat_log)} {prompt}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=150
    )
    message = response.choices[0].text.strip()
    chat_log.append(message)
    return message, chat_log

while True:
    user_input = input("You: ")
    if user_input.lower() in ("bye", "goodbye", "exit"):
        print("Chatbot: Goodbye!")
        break
    response, chat_log = get_response(user_input, chat_log)
    print("Chatbot:", response)
