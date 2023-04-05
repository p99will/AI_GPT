import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re

model       = "gpt-3.5-turbo"
temperature = 0.1

msgs = [] # list of messages for openai

def talk(myMsg):
    msgs.append({"role": "user", "content": myMsg})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
        temperature=temperature
    )
    reply = completion.choices[0].message.content
    msgs.append(completion.choices[0].message)
    return add_syntaxHighlighting(reply)
    
    
def add_syntaxHighlighting(msg):
    code_snippets = re.findall(r"```(.*?)```", msg, re.DOTALL)
    snippets = []
    for code in code_snippets:
        if(len(code) != 0): 
            highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
            snippets.append(highlighted_code)
    for i in range(len(code_snippets)):
        msg = msg.replace("```" + code_snippets[i] + "```", snippets[i])

    return msg