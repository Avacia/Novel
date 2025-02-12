import sys
import os
import json
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from novelScrapper import NovelScraper, NovelConfig

logger = logging.getLogger(__name__)

def load_json_config(json_path: str) -> dict:
    """Load and return configuration from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_book_name() -> str:
    """Get book name from stdin or user input"""
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())['bookName']
    return input("Book name: ")

def create_config_from_json(data: dict) -> NovelConfig:
    """Create NovelConfig instance from JSON data"""
    return NovelConfig(
        book_name=data['book_name'],
        menu_url=data['menu_url'],
        multi_page=data['multi_page'],
        page_css=data['page_css'],
        page_link=data['page_link'],
        title_css=data['title_css'],
        body_css=data['body_css'],
        unwanted_selector=data['unwanted_selector']
    )

def get_interactive_config(book_name: str) -> NovelConfig:
    """Create NovelConfig instance from user input"""
    return NovelConfig(
        book_name=book_name,
        menu_url=input("Menu URL: "),
        multi_page=input("Multi-page CSS (optional): "),
        page_css=input("Page CSS: "),
        page_link=input("Page link: "),
        title_css=input("Title CSS: "),
        body_css=input("Body CSS: "),
        unwanted_selector=input("Unwanted selector (optional): ")
    )

def main():
    scraper = NovelScraper()
   
    try:
        book_name = get_book_name()
        json_path = os.path.join('JSON', f"{book_name}.json")

        if os.path.exists(json_path):
            config = create_config_from_json(load_json_config(json_path))
            logger.info(f"Using existing configuration for: {book_name}")
        else:
            config = (create_config_from_json(json.loads(sys.stdin.read()))
                     if not sys.stdin.isatty()
                     else get_interactive_config(book_name))

        print(f"\nStarting to process {book_name}...")
        
        # Get chapter URLs first
        html = scraper.fetch_page(config.menu_url)
        urls = scraper.parse_content(html, config.page_css, config.page_link)
        total_chapters = len(urls)
        
        # Create book path
        book_path = scraper.books_path / config.book_name
        book_path.mkdir(exist_ok=True)
        
        # Save book configuration
        config_file = scraper.json_path / f"{config.book_name}.json"
        config_file.write_text(json.dumps(vars(config), indent=4), encoding='utf-8')
        
        # Process chapters with progress bar
        with tqdm(total=total_chapters, desc="Processing chapters") as pbar:
            with ThreadPoolExecutor() as executor:
                futures = []
                for i in range(total_chapters):
                    future = executor.submit(scraper.process_chapter, i, urls, config, book_path)
                    future.add_done_callback(lambda x: pbar.update(1))
                    futures.append(future)
                
                # Wait for all futures to complete
                for future in futures:
                    future.result()
            
        print(f"\nProcessing complete for {book_name}!")
        logger.info(f"Successfully processed book: {config.book_name}")
       
    except Exception as e:
        logger.error(f"Error processing book: {str(e)}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
