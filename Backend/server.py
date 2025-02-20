from flask import Flask, jsonify, request
from subprocess import run
from flask_cors import CORS
import json
from http import HTTPStatus
from novelLibrary import NovelLibrary


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    library = NovelLibrary()

    @app.route('/')
    def health_check():
        return jsonify({"status": "healthy", "message": "Server is running"})

    @app.route('/booksMenu', methods=['GET'])
    def get_books():
        try:
            books_data = {"books": library.books_metadata}
            return jsonify(books_data)
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR    
            
    @app.route("/booksMenu/<int:book_id>", methods=['GET'])
    def get_book_by_id(book_id):
        try:
            folder_name, chapters = library.get_book_info(book_id)
            return jsonify({
                "book_id": book_id,
                "folder_name": folder_name,
                "chapters": chapters
            })
        except ValueError as e:
            return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.route("/booksMenu/<int:book_id>/chapter/<int:chapter_id>", methods=["GET"])
    def get_chapter(book_id, chapter_id):
        try:
            chapter_data = library.get_chapter_content(book_id, chapter_id)
            return jsonify(chapter_data)
        except FileNotFoundError:
            return jsonify({"error": "Chapter not found"}), HTTPStatus.NOT_FOUND
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.route("/addBooks", methods=['POST'])
    def add_books():
        try:
            novel_data = request.get_json()
            print(novel_data)
            result = run(["python", "getNovelContent.py"], 
                        input=json.dumps(novel_data),
                        capture_output=True, 
                        text=True)
            if result.returncode == 0:
                return jsonify({"message": "Books added successfully"}), HTTPStatus.OK
            return jsonify({"error": result.stderr}), HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    return app

if __name__ == '__main__':
    print("Starting Flask server...")
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
    