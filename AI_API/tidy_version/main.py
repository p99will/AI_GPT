from imports import *

# -------- Consts --------
debugging = True

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


def ai_talk(msg):
    htmlMSG = []
    # htmlMSG.append('<div class="container">')
    # htmlMSG.append('    <div class="AI_MSG">')
    # htmlMSG.append('        <div class="msg_from"> AI: </div>')
    # htmlMSG.append('        <div class="container">')
    # htmlMSG.append(msg)
    htmlMSG.append(r'''
                   
<div class="container">
<div class="AI_MSG">
<div class="msg_from"> AI: </div>
''')
    

def reset_AI():
    msgs.clear()
    return ai_talk("Okay. lets start over.")

def process_message(msg):
     if(msg == "reset"):
        return reset_AI()

if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000") 
    app.run(debug=debugging)