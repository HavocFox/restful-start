from flask import Flask, jsonify, request #importing the Flask class
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from sql_connect import connect_db, Error

app = Flask(__name__)
ma = Marshmallow(app)

#Creating the Book Table Schema, to define the structure of data
class BookSchema(ma.Schema):
    id = fields.Int(dump_only=True)         # dump_only means we dont input data for this field
    title = fields.String(required=True)    # required means to be valid need a value
    isbn = fields.String(required=True)
    publication_date = fields.String(required=True)
    availability = fields.Boolean(required=True)

    class Meta:
        fields = ("title", "isbn", "publication_date", "availability")

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/') #Defining a simple home route, which recieves requests
def home():
    return "Welcome to the Flask Party" #returning a response 



#Creating a new book with a POST request
@app.route('/books', methods=['POST'])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # new_book details
            new_book = (book_data['title'], book_data['isbn'], book_data['publication_date'])

            # query
            query = "INSERT INTO Books (title, isbn, publication_date) VALUES (%s, %s, %s)"

            # Execute query with new_book data
            cursor.execute(query, new_book)
            conn.commit()

            return jsonify({'Message': "New Book Added Successfully!"}), 201
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database Connection failed"}), 500
    

if __name__ == '__main__': #idom to verify we're running this selected file, and not allow running if imported 
    app.run(debug=True)