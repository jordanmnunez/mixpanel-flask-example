# Web server libraries
from flask import Flask, redirect, render_template, request

# Initiate web-app
app = Flask(__name__)

app.debug = True
app.secret_key = 'development'

# The app.route() wrapper handles request addresses coming in
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/registration.html')
def registration():
    return render_template('registration.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    # Starts the server on all IPs for the host on a port 8000
    app.run(host='0.0.0.0', port=8000)
