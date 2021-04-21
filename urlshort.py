from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify
import json
import os.path

app = Flask(__name__)
app.secret_key='abarakadabra'



@app.route('/')
def index():
    return render_template('index.html',codes=session.keys())

@app.route('/your-url',methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys() :
            flash('short name already taken try another value')
            return redirect(url_for('index'))

        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']]=True

        return render_template('your_url.html' , code = request.form['code'])
    else:
        return redirect(url_for('index'))

@app.route('/clearAPI')
def deleteAPI():
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
    for key in list(session.keys()):
        if key not in urls.keys():
            session.pop(key)
    flash('Session APIs not in file Removed')
    return redirect(url_for('index'))

@app.route('/clearAPI/<string:key_API>')
def removeAPI(key_API):
    session.pop(key_API)
    flash('key_API removed from sessions')
    return redirect(url_for('index'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys() :
                    return redirect(urls[code]['url'])

    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
