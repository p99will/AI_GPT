import openai
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define function to generate chat response
def generate_chat_response(prompt, model, temperature=0.5, max_tokens=50, stop=None, context=None):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        # context=context,
        stream=True
    )

    message = response.choices[0].text.strip()
    context += message
    return message, context

# Define function to handle conversation
def chat(model, temperature=0.5, max_tokens=50, stop=None):
    print("Bot: Hi, how can I assist you today?")
    context = ""
    while True:
        prompt = input("You: ")
        if prompt.lower() == "exit":
            print("Bot: Goodbye!")
            break
        response, context = generate_chat_response(prompt, model, temperature, max_tokens, stop, context)
        print("Bot:", response)

# Example usage
model = "text-davinci-002"
chat(model)
