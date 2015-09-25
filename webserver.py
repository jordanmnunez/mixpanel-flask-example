# Web server libraries
from flask import Flask, flash, redirect, render_template, request

from mixpanel import Mixpanel
import json
from urllib import unquote
import uuid

# Initiate web-app
app = Flask(__name__)

app.debug = True
app.secret_key = 'development'

# Mixpanel tracking
MP_TOKEN = 'jordan'
mixpanel = Mixpanel(MP_TOKEN)

# Fake Database
DB = {
    'users': {}
}

# Mixpanel cookie parser
def cookie_to_mixpanel_data(cookie, token):
    mp_cookie_name = "mp_%s_mixpanel" % token
    mp_cookie = cookie.get(mp_cookie_name)
    return json.loads(unquote(mp_cookie).decode('utf8'))

# Fake function that would simulate writting a user to your dabatse
def create_user(form, cookie):
    if request.form['email'] not in DB['users']:
        DB['users'][request.form['email']] = {
            'alias': request.form['email'],
            'distinct_id': cookie['distinct_id'],
            '$first_name': request.form['fn'],
            '$last_name': request.form['ln'],
            '$email': request.form['email'],
            'Favourite Genre': request.form['genre'],
            'udid': str(uuid.uuid4()),
        }

        return DB['users'][request.form['email']]
    else:
        return None

# The app.route() wrapper handles request addresses coming in
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/registration.html', methods = ['GET', 'POST'])
def registration():
    if request.method == "POST":
        cookie = cookie_to_mixpanel_data(request.cookies, MP_TOKEN)
        user_info = create_user(request.form, cookie)
        if user_info:
            mixpanel.alias(user_info['alias'], user_info['distinct_id'])
            mixpanel.track(user_info['distinct_id'], 'Signup', user_info, meta={'$ip':0})
            mixpanel.people_set(user_info['distinct_id'], user_info, meta={'$ip':0, '$ignore_time':True})
            return redirect('home.html')
        else:
            flash(u'This email already exists', 'error')
            return redirect('registration.html')
    else:
        return render_template('registration.html')

@app.route('/home.html')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    # Starts the server on all IPs for the host on a port 8000
    app.run(host='0.0.0.0', port=8000)
