from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import sqlite3


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

def delet(dell):
    con = sqlite3.connect('static/Portfolio.db')
    cur = con.cursor()
    cur.execute(f"DELETE FROM todos WHERE todo = '{dell}'")
    con.commit()
    return show()

def insert(new):
    con = sqlite3.connect('static/Portfolio.db')
    cur = con.cursor()
    cur.execute("""SELECT rowid
              FROM    todos;""")
    data = cur.fetchall()
    data = [x[0] for x in data]
    item = max(data)
    ne = item + 2
    #print(ne)
    cur.execute(f"INSERT INTO todos VALUES ('item{ne}', '{new[0]}', ' ', '{new[1]}')")
    con.commit()
    con.close()
    return show()

def show():
    con = sqlite3.connect('static/Portfolio.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM todos")
    data = cur.fetchall()
    con.close()
    return data

def update(lst):
    if lst == []:
        #print('triggered')
        con = sqlite3.connect('static/Portfolio.db')
        cur = con.cursor()
        cur.execute(f"UPDATE todos SET if = ' '")
        con.commit()
        con.close()
        #print('done')
        return show()
    else:
        item = tuple(lst+['bo'])
        #print(item)
        con = sqlite3.connect('static/Portfolio.db')
        cur = con.cursor()
        cur.execute(f"UPDATE todos SET if = ' ' WHERE todo NOT IN {item}")
        cur.execute(f"UPDATE todos SET if = 'checked' WHERE todo IN {item}")
        con.commit()
        con.close()
        return show()

@app.route('/', methods=['GET', 'POST'])
def hello():
    data = show()
    if request.method == 'POST':
        new = request.form.getlist('newtask')
        print(new)
        if new != []:
            data = insert(new)
        up = request.form.getlist('item')
        print(up)
        if new == [] and up != []:
            data = update(up)
        if new == [] and up == []:
            data = update(up)
        return render_template('index.html', data=data)
    return render_template('index.html', data=data)

@app.route('/del/<placeholder>')
def dol(placeholder):
    delet(placeholder)
    return redirect('/')


if __name__ == '__main__':
     app.run(debug=True)

