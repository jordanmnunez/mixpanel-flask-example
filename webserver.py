# Web server libraries
from flask import Flask, redirect, render_template, request
from urllib import unquote
import json

# Initiate web-app
app = Flask(__name__)

app.debug = True
app.secret_key = 'development'

MP_TOKEN = 'jordan'

# Mixpanel cookie parser
def cookie_to_mixpanel_data(cookie, token):
    mp_cookie_name = "mp_%s_mixpanel" % token
    mp_cookie = cookie[mp_cookie_name]
    return json.loads(unquote(mp_cookie).decode('utf8'))

# The app.route() wrapper handles request addresses coming in
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/registration.html', methods = ['GET', 'POST'])
def registration():
    if request.method == "POST":
        print cookie_to_mixpanel_data(request.cookies, MP_TOKEN)['distinct_id']
        return redirect('home.html')
    else:
        return render_template('registration.html')

@app.route('/home.html')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    # Starts the server on all IPs for the host on a port 8000
    app.run(host='0.0.0.0', port=8000)
