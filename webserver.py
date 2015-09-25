# Web server libraries
from flask import Flask, redirect, render_template, request
from urllib import unquote
import json
from mixpanel import Mixpanel

# Initiate web-app
app = Flask(__name__)

app.debug = True
app.secret_key = 'development'

# Mixpanel tracking
MP_TOKEN = 'jordan'
mixpanel = Mixpanel(MP_TOKEN)

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
        cookie = cookie_to_mixpanel_data(request.cookies, MP_TOKEN)
        user_info = {
            'alias': request.form['email'],
            'distinct_id': cookie['distinct_id'],
            '$first_name': request.form['fn'],
            '$last_name': request.form['ln'],
            '$email': request.form['email'],
            'Favourite Genre': request.form['genre'],
            }
        mixpanel.alias(user_info['alias'], user_info['distinct_id'])
        mixpanel.track(user_info['distinct_id'], 'Signup', user_info, meta={'$ip':0})
        mixpanel.people_set(user_info['distinct_id'], user_info, meta={'$ip':0, '$ignore_time':True})
        return redirect('home.html')
    else:
        return render_template('registration.html')

@app.route('/home.html')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    # Starts the server on all IPs for the host on a port 8000
    app.run(host='0.0.0.0', port=8000)
