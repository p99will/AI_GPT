from imports import *
from model import *
import openai  

# -------- Consts --------
debugging = False                      # Set to True to enable debugging
pagebreak = '<hr class="hr-primary">'  # HTML for a page break

# -------- Objects --------
app = Flask(__name__)
# Get the OpenAI API key from the environment variables - See README.md for more info
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------- Functions --------


@app.route('/syntax.css')
def CSS_Syntax():
    return app.send_static_file('syntax.css')


@app.route('/style.css')
def CSS():
    return app.send_static_file('style.css')


@app.route('/')
def index():
    return app.send_static_file('index.html')

# This function handles a POST request to send a message, processes it, adds HTML formatting, and returns the result with a page break.


@app.route('/send_message', methods=['POST'])
def send_message():
    # get the message from the request
    message = request.form['message']
    # process the message, and get the AI's responce
    HTMLresponce = process_message(message)
    # add HTML formatting to the message
    HTMLmessage = addHTML(message.replace('\n', '<br>'), "Me")
    debug(HTMLresponce)
    # return the message and the AI's responce with a page break
    return HTMLmessage + HTMLresponce + pagebreak


# This function takes in a message and a user, and returns an HTML-formatted message with the user's name and the message content.
# It replaces placeholders in an HTML template with the message and user information.
def addHTML(msg, user):
    htmlMSG = '''             
<div class="container">
    <div class="AI_MSG">
        <div class="msg_from"><b>{|usr|}:</b> </div>
        <div class="container">
            {|msg|}
        </div>
    </div>
</div>
'''.replace("{|msg|}", msg).replace("{|usr|}", user)
    return ''.join(htmlMSG)


# This function resets the AI
def reset_AI():
    msgs.clear()
    return addHTML("Okay. lets start over.", "AI")


# Processes a message
def process_message(msg):
    if(msg == "reset"):
        return reset_AI()
    return addHTML(talk(msg), "AI")


def debug(msg):
    if(debugging):
        print(msg)


if __name__ == '__main__':
    # Open the web page in the default browser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=debugging)
