from flask import Flask, jsonify, request, render_template, redirect, make_response
from functools import wraps
#comment

app = Flask(__name__)

def auth_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if auth and auth.username == 'sarah' and auth.password == 'luna':
      return f(*args, **kwargs)
    return make_response("<h1>Access Denied! Could not verify your login!</h1>", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
  return decorated

books = [
    {"id": 1, "author": "Albert Camus", "title": "The Stranger", "price": 12.49},
    {"id": 2, "author": "Franz Kafka", "title": "The Metamorphosis", "price": 9.49},
    {"id": 3, "author": "George Orwell", "title": "1984", "price": 15.95},
    {"id": 4, "author": "Henrik Ibsen", "title": "A Doll's House", "price": 11.49},
    {"id": 5, "author": "Vladimir Nabokov", "title": "Lolita", "price": 8.99},
    {"id": 6, "author": "Charles Dickens", "title": "Great Expectations", "price": 11.49},
    {"id": 7, "author": "Unknown", "title": "One Thousand and One Nights", "price": 28.99},
    {"id": 8, "author": "Johann Wolfgang von Goethe", "title": "Faust", "price": 18.99},
    {"id": 9, "author": "Gustave Flaubert", "title": "Madame Bovary", "price": 8.99}
]

#curl http://localhost:5000
@app.get('/')
@auth_required
def index():
    return render_template('base2.html', data = books)

#curl http://localhost:5000/books
@app.get('/books')
def hello():
  return jsonify(books)

#curl http://localhost:5000/book/1
@app.get('/book/<int:id>')
def get_book(id):
    for book in books:
    if book["id"] == id:
        return jsonify(book)
  return f'Book with id {id} not found', 404

#curl http://localhost:5000/add_book --request POST --data '{"id":3,"author":"aaa","title":"bbb","price":99.99}' --header "Content-Type: application/json"
@app.post("/add_book")
def add_book():
  #data = request.get_json()
  new_id = int(request.form['id'])
  new_title = request.form['title']
  new_author = request.form['author']
  new_price = float(request.form['price'])
  new_book = {"id": new_id, "title": new_title, "author": new_author, "price": new_price }
  books.append(new_book)
  return redirect('/')

#curl http://localhost:5000/update_book/2 --request POST --data '{"author":"ccc","title":"ddd","price":999.99}' --header "Content-Type: application/json"
@app.route('/update_book/<int:id>', methods=['GET','POST'])
@auth_required
def update_book(id):
  for book in books:
    if book["id"] == id:
        if request.method=="POST":
          book["id"] = int(request.form['id'])
          book["title"] = request.form['title']
          book["author"] = request.form['author']
          book["price"] = float(request.form['price'])
          return redirect('/')
        else:
          return render_template('update.html', book = book)
  return f'Book with id {id} not found', 404

#curl http://localhost:5000/delete_book/1 --request DELETE
@app.route('/delete_book/<int:id>', methods=['GET','POST'])
@auth_required
def delete_book(id):
  for book in books:
    if book["id"] == id:
        if request.method=="POST":
          books.remove(book)
          return redirect('/')
        else:
          return render_template('delete.html', book = book)
  return f'Book with id {id} not found', 404
