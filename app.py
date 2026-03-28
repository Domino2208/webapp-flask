from flask import Flask, render_template, url_for, request, redirect
from dotenv import load_dotenv
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect (
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/')
def index():
    return render_template('index.html', URL_STATIC=url_for('static', filename=''))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/danke')

@app.route('/danke')
def danke():
    return render_template('danke.html', URL_STATIC=url_for('static', filename=''))

if __name__ == '__main__':
    app.run (
        debug=True,
        host='0.0.0.0',
        port=5000
    )