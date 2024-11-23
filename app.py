from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Koneksi ke database
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='wensen',
        password='12345',
        database='money_management'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = request.form['amount']
    date = request.form['date']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (description, amount, date) VALUES (%s, %s, %s)', (description, amount, date))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
