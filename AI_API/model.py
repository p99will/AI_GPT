import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re


model = "gpt-3.5-turbo"
temperature = 0.1   # 0.1 - 1.0

msgs = []  # list of messages for openai

pre_code_snippet = '''
'''

post_code_snippet = ''

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

# This function takes in a message and searches for code snippets enclosed in triple backticks. EG: ```print("Hello World")```
# It then uses the Pygments library to highlight the code snippets with syntax highlighting and replaces the original code snippets with the highlighted versions. 
# The function returns the message with syntax highlighting added to any code snippets found.
def add_syntaxHighlighting(msg):
    code_snippets = re.findall(r"```(.*?)```", msg, re.DOTALL)
    snippets = []
    for code in code_snippets:
        if(len(code) != 0):
            highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
            snippets.append(highlighted_code)
    for i in range(len(code_snippets)):
        msg = msg.replace("```" + code_snippets[i] + "```", pre_code_snippet + snippets[i] + post_code_snippet)

    return msg
