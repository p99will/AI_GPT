import openai

# !pip install pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# !pip install regex
import re


# The model to use. See https://beta.openai.com/docs/developer-quickstart for more info
model = "gpt-3.5-turbo"
temperature = 0.5   # 0.0 - 1.0
#   0.0 = AI will always choose the most likely response. 1.0 = AI will choose a random response.


msgs = []  # list of messages.


# This function takes in a message and uses OpenAI's Chat API to generate a response.
# It appends the user's message to a list of messages, sends the list to the API, and retrieves the response.
# The response is then appended to the list of messages and returned with syntax highlighting added using the "add_syntaxHighlighting" function.
def talk(myMsg):
    msgs.append({"role": "user", "content": myMsg})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
        temperature=temperature
    )
    reply = completion.choices[0].message.content
    msgs.append(completion.choices[0].message)
    return add_syntaxHighlighting(reply).replace('\n', '<br>').replace('<br><br>', '<br>')
    # This last bit of code replaces double line breaks with single line breaks to make the response look nicer.

# This function takes in a message and searches for code snippets enclosed in triple backticks. EG: ```print("Hello World")```
# It then uses the Pygments library to highlight the code snippets with syntax highlighting and replaces the original code snippets with the highlighted versions.
# The function returns the message with syntax highlighting added to any code snippets found.


def add_syntaxHighlighting(msg):
    # Finds all code snippets enclosed in triple backticks
    code_snippets = re.findall(r"```(.*?)```", msg, re.DOTALL)
    snippets = []  # List of highlighted code snippets
    for code in code_snippets:
        if(len(code) != 0):  # If the code snippet is not empty
            highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
            snippets.append(highlighted_code)
    # Replaces the original code snippets with the highlighted versions in the message
    for i in range(len(code_snippets)):
        msg = msg.replace("```" + code_snippets[i] + "```", snippets[i])

    return msg
