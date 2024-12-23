from flask import Flask, jsonify
import os


def getFileFromFolder(filePath):
    files = []
    for filename in os.listdir(filePath):
        fileLocation = os.path.join(filePath, filename)
        
        if os.path.isfile(fileLocation):
            files.append(filename)
            
    return files


try:
    bookPath = os.path.join(os.getcwd(), "Books")
    folders = [folder for folder in os.listdir(bookPath) if os.path.isdir(os.path.join(bookPath, folder))]

except Exception as e:
    print("Error initializing book folders:", str(e))
    folders = []
   
    
app = Flask(__name__)


@app.route('/')
def server():
    return "Server is successfully connected!!!"


@app.route('/booksMenu', methods=['GET'])
def getBooks():
    try:
        return jsonify({"Folders": folders})
    
    except FileNotFoundError:
        return jsonify({"Error": "Book folder not found"}), 404
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route("/booksMenu/<int:book_id>", methods=['GET'])
def getBooksByID(book_id):
    try:
        if book_id - 1 < 0 or book_id > len(folders):
            return jsonify({"Error": "Book ID out of range"}), 404

        folder_name = folders[book_id - 1]
        filePath = os.path.join(bookPath, folder_name)
        chapter = getFileFromFolder(filePath)
        return jsonify({"Book id": book_id, "Folder Name": folder_name, "Chapter": chapter})
    
    except FileNotFoundError:
        return jsonify({"Error": "Book folder not found"}), 404
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route("/addBooks", methods=['POST'])
def addBooks():
    try:
        os.system("python getNovelContent.py")
        return jsonify({"message": "Books have been added successfully"}), 200
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask server...")
    print("Initializing server setup...")
    app.run(debug=True)