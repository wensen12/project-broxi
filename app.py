from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="wenn",
    user="root",
    password="1234",
    database="mydatabase"
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
        db.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("UPDATE items SET name = %s WHERE id = %s", (name, id))
        db.commit()
        return redirect('/')
    
    cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
    item = cursor.fetchone()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM items WHERE id = %s", (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
