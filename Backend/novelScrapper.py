from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
import logging
import requests
import json
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NovelConfig:
    book_name: str
    menu_url: str
    multi_page: str
    page_css: str
    page_link: str
    title_css: str
    body_css: str
    unwanted_selector: str

class NovelScraper:
    def __init__(self):
        self.base_path = Path.cwd()
        self.books_path = self.base_path / "Books"
        self.json_path = self.base_path / "JSON"
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        self.books_path.mkdir(exist_ok=True)
        self.json_path.mkdir(exist_ok=True)

    def fetch_page(self, url: str) -> str:
        """Fetch and clean webpage content"""
        response = requests.get(url)
        response.raise_for_status()
        return re.sub(r'&#x[a-f0-9]{4};', "", response.text)

    def parse_content(self, html: str, selector: str, base_url: Optional[str] = None) -> List[str]:
        """Parse HTML content using BeautifulSoup"""
        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select(selector)
        
        if base_url:
            return [f"{base_url}{element['href']}" for element in elements]
        return [element.get_text(strip=True) for element in elements]

    def save_chapter(self, chapter_num: int, title: List[str], content: List[str], book_path: Path):
        """Save chapter data to JSON file"""
        chapter_data = {
            "Title": title,
            "Paragraph": content
        }
        chapter_file = book_path / f"Chapter {chapter_num}.json"
        chapter_file.write_text(json.dumps(chapter_data, indent=4, ensure_ascii=False), encoding='utf-8')

    def process_chapter(self, index: int, urls: List[str], config: NovelConfig, book_path: Path):
        """Process individual chapter"""
        logger.info(f"Processing chapter {index + 1}/{len(urls)}")
        html = self.fetch_page(urls[index])
        title = self.parse_content(html, config.title_css)
        content = self.parse_content(html, config.body_css)
        self.save_chapter(index + 1, title, content, book_path)

    def process_book(self, config: NovelConfig):
        """Process entire book"""
        book_path = self.books_path / config.book_name
        book_path.mkdir(exist_ok=True)
        
        # Save book configuration
        config_file = self.json_path / f"{config.book_name}.json"
        config_file.write_text(json.dumps(vars(config), indent=4), encoding='utf-8')

        # Get chapter URLs
        if config.multi_page:
            urls = self._handle_multi_page(config)
        else:
            html = self.fetch_page(config.menu_url)
            urls = self.parse_content(html, config.page_css, config.page_link)

        # Process chapters concurrently
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.process_chapter, i, urls, config, book_path)
                for i in range(len(urls))
            ]
            for future in futures:
                future.result()  # Raise any exceptions that occurred

    def _handle_multi_page(self, config: NovelConfig) -> List[str]:
        """Handle multi-page menu scraping"""
        all_urls = []
        page_num = 1
        while True:
            page_url = config.menu_url.replace("{i}", str(page_num))
            html = self.fetch_page(page_url)
            urls = self.parse_content(html, config.page_css, config.page_link)
            if not urls:
                break
            all_urls.extend(urls)
            page_num += 1
        return all_urls
