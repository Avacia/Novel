from flask import Flask, jsonify
from flask_cors import CORS
import json
import os


def extractNumberFromFile(file):
    return int(file.split()[1].split(".")[0])


def getFileFromFolder(filePath):
    files = []
    for filename in sorted(os.listdir(filePath), key=extractNumberFromFile):
        fileLocation = os.path.join(filePath, filename)
        
        if os.path.isfile(fileLocation):
            files.append(filename)
            
    return files


def getBooks():
    for file in os.listdir(jsonPath):
        filePath = os.path.join(jsonPath, file)

        if file.endswith(".json"):
            with open(filePath, "r", encoding='utf-8') as jsonFile:
                data = json.load(jsonFile)
                folders.append(data)

def booksID(id):
    try:
        if id - 1 < 0 or id > len(folders):
            return jsonify({"Error": "Book ID out of range"}), 404

        folderName = folders[id - 1].get("Name")
        currentfilePath = os.path.join(bookPath, folderName)
        chapter = getFileFromFolder(currentfilePath)
    
        return folderName, chapter

    except FileNotFoundError:
        print(jsonify({"Error": "Book folder not found"}), 404)
    
    except Exception as e:
        print(jsonify({"Error": str(e)}), 500)


try:
    bookPath = os.path.join(os.getcwd(), "Books")
    jsonPath = os.path.join(os.getcwd(), "JSON")
    folders = []
    getBooks()
    

except Exception as e:
    print("Error initializing book folders:", str(e))
   
    
app = Flask(__name__)
CORS(app)


@app.route('/')
def server():
    return "Server is successfully connected!!!"


@app.route('/booksMenu', methods=['GET'])
def getbookMenu():
    return jsonify({"Folders": folders})


@app.route("/booksMenu/<int:book_id>", methods=['GET'])
def getBooksByID(book_id):
    try:
        folderName, chapter = booksID(book_id)
        return jsonify({"Bookid": book_id, "FolderName": folderName, "Chapter": chapter})
    
    except FileNotFoundError:
        return jsonify({"Error": "Book folder not found"}), 404
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route("/booksMenu/<int:book_id>/chapter/<int:chapter_id>", methods=["GET"])
def getChapterId(book_id, chapter_id):
    try:
        folderName, chapter = booksID(book_id)
        currentfilePath = os.path.join(bookPath, folderName)
        chapterName = os.path.join(currentfilePath, f"Chapter {chapter_id}.json")
        print(chapterName)
        with open(chapterName, "r", encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)

        return jsonify({"Title": data["Title"], "Paragraph": data["Paragraph"]})

    except FileNotFoundError:
        return ({"Error": "Chapter not found!"})

    except Exception as e:
        return ({"Error" : str(e)}) 



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