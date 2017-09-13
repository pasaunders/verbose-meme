from flask import Flask, request, redirect, render_template, session, flash
import re

# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "supersecret"

# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'emails')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/success', methods=['POST'])
def success():
    if EMAIL_REGEX.match(request.form['email']):
        query = 'INSERT INTO emails (email, created) VALUES (:email, NOW())'
        data = {
            'email': request.form['email'],
        }
        mysql.query_db(query, data)
        query = 'SELECT * FROM emails;'
        emails = mysql.query_db(query)
        flash('The email address you entered ({}) is valid.'.format(request.form['email']))
        return render_template('success.html', emails=emails)
    else:
        flash('email not valid')
        return redirect('/')

# @app.route('/update_friend/<friend_id>', methods=['POST'])
# def update(friend_id):
#     query = 'UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id'
#     data = {
#         'first_name': request.form['first_name'],
#         'last_name': request.form['last_name'],
#         'occupation': request.form['occupation'],
#         'id': friend_id,
#     }
#     mysql.query_db(query, data)
#     return redirect('/')


# @app.route('/remove_friend/<friend_id>', methods=['POST'])
# def delete(friend_id):
#     query = "DELETE FROM friends WHERE id = :id"
#     data = {'id': friend_id}
#     mysql.query_db(query, data)
#     return redirect('/')


# @app.route('/friends/<friend_id>')
# def show(friend_id):
#     query = "SELECT * FROM friends WHERE id = :specific_id"
#     data = {'specific_id': friend_id}
#     friends = mysql.query_db(query, data)
#     return render_template('index.html', one_friend=friends[0])


app.run(debug=True)
