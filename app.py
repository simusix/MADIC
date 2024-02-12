from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
import mysql.connector
from config import Config
import json, sqlite3

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'secrets' # for now just to supress warnings

mail = Mail(app)

mydb = mysql.connector.connect(
  host=app.config["MYSQL_HOST"],
  user=app.config["MYSQL_USER"],
  password=app.config["MYSQL_PASSWORD"],
  database=app.config["MYSQL_DB"]
)

cur = mydb.cursor(buffered=True)

vars = {'english': 'anj_preklad', 'slovak': 'sk_preklad'}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dictionary')
def dictionary():
    cur.execute("SHOW COLUMNS FROM anj")
    columns = [column[0] for column in cur.fetchall()]
    
    query = "SELECT "
    for column in columns:
        query += f"COALESCE({column}, ' ') AS {column}, "
    query = query[:-2] + " FROM anj ORDER BY sk_preklad ASC"
    
    cur.execute(query)
    data = cur.fetchall()
    
    return render_template('dictionary.html', data=data)

@app.route('/contact')
def contact():

    return render_template('contact.html')

def send_email(type, sender, recipients, body):
       msg = Message(subject=f'MADIC {type}', sender=sender[0], recipients=recipients)
       msg.html = f"""
                   <h1>Message to MADIC</h1>
                   <b>From</b> 
                   <p>{sender[0]} ({sender[1]} {sender[2]})</p>
                   <b>Message type</b>
                   <p>{type}</p>

                   <b>Message</b>
                   <p>{body}</p>
                   """
       mail.send(msg)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        type = request.form['type']
        msg = request.form['message']
        send_email(type, [email,firstname,lastname], [app.config["MAIL_USERNAME"]], msg)
        flash('Ďakujeme vám za váš príspevok ', 'success')
    except Exception as e:
        flash(f'Chyba pri odoslaní: {e}', 'error')
        
    return redirect(url_for('contact'))

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/get_toggled_status') 
def toggled_status():
  current_status = request.args.get('status')
  new_status = 'slovak' if current_status == 'english' else 'english'
  return jsonify(new_status=new_status)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    language = request.args.get('status')
    suggestions = get_suggestions(query, language)
    return jsonify(suggestions=suggestions)

def get_suggestions(query, language):
    # TODO: Lots of queries at once. Maybe make a try except to catch connection loss to sql server

    cur.execute("""
                   SELECT {0}
                   FROM anj 
                   WHERE {0} LIKE %s
                   LIMIT 10
                """.format(vars[language]),
                (f'%{query}%',))
    
    rows = cur.fetchall()
    for row in rows:
        print(row[0].capitalize())
        print("---")
    suggestions = [row[0].title() for row in rows]
    return suggestions

@app.route('/search', methods=['POST'])
def search():
    query = request.form['term'].lower()
    language = request.form['current_status']
    

    cur.execute("""
                   SELECT {0}, sk_znak, anj_znak, popis
                   FROM anj 
                   WHERE {1} LIKE %s
                """.format(vars['english' if language != 'english' else 'slovak'], vars[language]),
                (f'%{query}%',))

    try:
        results = cur.fetchall()[0]
    except IndexError:
        results = None

    if results is None or query == '':
        return jsonify({"translation": "Translation not found"})


    return jsonify({"translation": results[0], "sk_znak": results[1], "anj_znak": results[2], "popis": results[3]})

if __name__ == '__main__':
    app.run(debug=True)

