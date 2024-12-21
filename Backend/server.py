from flask import Flask
import getNovelContent

app = Flask(__name__)
  

@app.route('/')
def server():
    return "Server is successfully connected!!!"


@app.route('/booksMenu', methods=['GET'])
def getBooks():
    return


@app.route("/booksMenu/<int:book_id>", methods=['GET'])
def getBooksByID(book_id):
    return


if __name__ == '__main__':
    app.run(debug=True)