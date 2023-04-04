from flask import Flask, request, jsonify
import os
import openai
import re
import webbrowser
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import requests

# -------- Objects --------
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------- Consts --------
debugging = True

buttonHTMLStart = '''
<div class="code-block row">
    <div class="col-md-10">
    <pre><code id="code-text">

'''
buttonHTMLEnd = '''
    </code></pre>
  </div>
  <div class="col-md-2">
    <button class="btn btn-secondary float-right" id="copy-button">Copy</button>
  </div>
</div>
'''


# -------- Vars --------
messages = [] # list of html messages
msgs = [] # list of messages for openai

# -------- Functions --------
@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    if(message == "reset"):
        msgs.clear()
        return jsonify('<div="myMSG">' + "<b>Me:</b> <br>" + message + "</div><br><br>"\
        + '<div="AIMSG">' + "<b>AI:</b> <br>" + "Okay. Lets start over." + '</div><br><hr class="hr-primary">')
    debug("User: " + message)
    reply = talk(message).replace('\n\n', '<br>').replace('\n', '<br>').replace('<br><br>', '<br>')
    debug("AI: " + reply)
    
    return jsonify('<div="myMSG">' + "<b>Me:</b> <br>" + message + "</div><br><br>"\
        + '<div="AIMSG">' + "<b>AI:</b> <br>" + reply + '</div><br><hr class="hr-primary">')


def showCode(myCode):
    snippets = []
    for code in myCode:
        if(len(code) == 0): return
        highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
        snippets.append(highlighted_code)
    return snippets

def debug(msg):
    if(debugging):
        print(msg)

def talk(myMsg):
    msgs.append({"role": "user", "content": myMsg})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgs,
        temperature=0.1
    )
    reply = completion.choices[0].message.content
    code_snippets = re.findall(r"```(.*?)```", completion.choices[0].message.content, re.DOTALL)
    # code_snippets.append( re.findall(r"`(.*?)`", completion.choices[0].message.content, re.DOTALL))
    highlighted_code = showCode(code_snippets)
    msgs.append(completion.choices[0].message)
    for i in range(len(code_snippets)):
        reply = reply.replace("```" + code_snippets[i] + "```",  buttonHTMLStart + highlighted_code[i] + buttonHTMLEnd)
                            #   '<button id="copyButton">Copy to Clipboard</button>')
    # response = requests.post("http://127.0.0.1:5000/recv_message", data={'message': reply, 'highlighted_code': highlighted_code})
    return reply


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000") 
    app.run(debug=debugging)