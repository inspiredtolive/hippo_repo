#!/usr/bin/python3
from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, render_template, redirect
import json
import os
# use loginpass to make OAuth connection simpler

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'pengwingsiscool'

oauth = OAuth(app)
oauth.register(
    name='github',
    client_id=os.getenv('CLIENT_ID') or '10a81c493f912828f09f',
    client_secret=os.getenv('CLIENT_SECRET') or 'cd6b2f37ab6b2e2991ef2c09bc918a8499d4af11',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user repo'},
)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user')
    profile = resp.json()
    resp = oauth.github.put(
        'repos/{}/monty/contents/test5.txt'.format(profile.get('login')),
        data=json.dumps({
            "message": "Initial Commit",
            "content": "bXkgbmV3IGZpbGUgY29udGVudHM="
        })
    )
    if resp.status_code == 201:
        return render_template('rhino.html', status='OK')
    return render_template('rhino.html', status='Failed to initialize file. File already exists.')


if __name__ == '__main__':
        if os.getenv('FLASK_ENV') == 'production':
            from waitress import serve
            serve(app, host='0.0.0.0', port=os.getenv('PORT', 80))
        app.run(host='0.0.0.0', port=5000)
