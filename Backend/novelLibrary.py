import os
import json
from typing import Tuple, List, Dict, Any


class NovelLibrary:
    def __init__(self):
        self.book_path = os.path.join(os.getcwd(), "Books")
        self.json_path = os.path.join(os.getcwd(), "JSON")
        self.books_metadata = []
        self._load_books_metadata()

    def _load_books_metadata(self) -> None:
        """Load metadata for all books from JSON files"""
        print(f"Loading books from: {self.json_path}")
        for file in os.listdir(self.json_path):
            if file.endswith(".json"):
                print(f"Found book file: {file}")
                with open(os.path.join(self.json_path, file), "r", encoding='utf-8') as json_file:
                    self.books_metadata.append(json.load(json_file))
        print(f"Total books loaded: {len(self.books_metadata)}")

    def get_chapter_files(self, folder_path: str) -> List[str]:
        """Get sorted list of chapter files from a book folder"""
        return sorted(
            [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
            key=lambda x: int(x.split()[1].split(".")[0])
        )

    def get_book_info(self, book_id: int) -> Tuple[str, List[str]]:
        """Get book folder name and chapter list"""
        if not 0 < book_id <= len(self.books_metadata):
            raise ValueError("Book ID out of range")
        
        folder_name = self.books_metadata[book_id - 1].get("book_name")
        book_path = os.path.join(self.book_path, folder_name)
        chapters = self.get_chapter_files(book_path)
        
        return folder_name, chapters

    def get_chapter_content(self, book_id: int, chapter_id: int) -> Dict[str, Any]:
        """Get content of a specific chapter"""
        folder_name, _ = self.get_book_info(book_id)
        chapter_path = os.path.join(self.book_path, folder_name, f"Chapter {chapter_id}.json")
        
        with open(chapter_path, "r", encoding='utf-8') as json_file:
            print(json_file)
            return json.load(json_file)