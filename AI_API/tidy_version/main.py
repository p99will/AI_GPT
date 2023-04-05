from imports import *
from model import *
import openai

# -------- Consts --------
debugging = True
pagebreak = '<hr class="hr-primary">'

# -------- Objects --------
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    HTMLresponce = process_message(message)
    HTMLmessage = addHTML(message, "Me")
    debug(HTMLresponce)
    return HTMLmessage + HTMLresponce + pagebreak


def addHTML(msg, user):
    htmlMSG = '''             
<div class="container">
    <div class="AI_MSG">
        <div class="msg_from"> {|usr|}: </div>
        <div class="container">
            {|msg|}
        </div>
    </div>
</div>
'''.replace("{|msg|}", msg).replace("{|usr|}", user)
    return ''.join(htmlMSG)
    

def reset_AI():
    msgs.clear()
    return addHTML("Okay. lets start over.", "AI")

def process_message(msg):
    if(msg == "reset"):
        return reset_AI()
    return addHTML(talk(msg), "AI")

def debug(msg):
    if(debugging):
        print(msg)
        
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000") 
    app.run(debug=debugging)