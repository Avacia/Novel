# Novel

## Backend - Novel Content Scraper and Flask API Server

This document provides details on two integrated components: a novel content scraper and a Flask API server to organize and serve the scraped content.

---

### Novel Content Scraper

This script is designed to scrape novel content from web pages, organize it into structured JSON files, and save the chapters into corresponding folders. The program is highly configurable and uses user inputs to define scraping behavior and file organization.

#### Features

- Fetch data from web pages using custom CSS selectors.
- Multi-page and single-page menu support.
- Organize chapters into structured folders.
- Save metadata and configuration in JSON files.
- Concurrent processing with ThreadPoolExecutor for faster chapter downloads.

#### Prerequisites

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `concurrent.futures` module

Install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

#### How It Works

1. **User Input or Existing Data:**
   - If a JSON file exists for a given book, the program loads its configuration.
   - Otherwise, the user is prompted to input menu URL, CSS selectors for titles and paragraphs, and other settings.

2. **Folder and File Management:**
   - Creates a folder structure for the book and chapters under the `Books` directory.
   - Stores configuration data in the `JSON` directory.

3. **Web Scraping:**
   - Fetches data from the specified URL using the provided CSS selectors.
   - Handles multi-page menus if applicable.

4. **Save Chapters:**
   - Each chapter is saved as a JSON file in the corresponding book folder.

#### Code Overview

##### Functions

- **`fetchDataFromWebMenu(link)`**: Fetches HTML content from a URL and cleans up unwanted characters.
- **`updateURL(url, pageNumber)`**: Replaces placeholders in a URL with the current page number.
- **`beautifulSoupFunction(data, itemCSS, needLink)`**: Parses HTML using BeautifulSoup to extract text or links based on CSS selectors.
- **`createBookFolder(bookName, folderPath)`**: Creates a directory for the book inside the `Books` folder.
- **`createBookInfo(...)`**: Saves book metadata and settings into a JSON file.
- **`getLinks(url, cssSelector, pageLink)`**: Fetches links from a page based on the provided CSS selector.
- **`createPages(...)`**: Downloads and saves chapter data concurrently using a thread pool.
- **`printProgressBar(...)`**: Displays a progress bar in the console during chapter processing.

##### Main Function
The `main()` function handles the overall workflow:

- Collects or loads user input.
- Sets up folders and files.
- Scrapes the web pages for chapters.
- Saves chapters as JSON files.

#### Error Handling
The script includes error handling for:

- Missing folders or files.
- Incorrect user inputs.
- Network or scraping errors.

#### Usage

1. Run the script using Python:

   ```bash
   python getNovelContent.py
   ```

2. Follow the prompts to input:
   - Book name
   - Menu URL
   - CSS selectors for chapters and content
   - Other necessary configurations

3. The script will:
   - Create a folder for the book in the `Books` directory.
   - Save chapters as JSON files inside the folder.

4. If a JSON file already exists for the book, the script will use its configuration.

---

### Flask API Server

The Flask API server serves as an interface for accessing the scraped novel data. It is designed to query and serve data in JSON format to front-end applications or other services.

#### Features

- Serve metadata and chapter data via RESTful endpoints.
- Load chapter content dynamically from stored JSON files.
- Easily configurable routes for various use cases.

#### Prerequisites

- Python 3.x
- `Flask` library

Install Flask using pip:

```bash
pip install Flask
```

#### Flask Application Structure

##### Endpoints

1. **`GET /booksMenu`**
   - Returns a list of all available books.
   - Example Response:
     ```json
     ["Book 1", "Book 2", "Book 3..."]
     ```

2. **`GET /booksMenu/<book_id>`**
   - Returns metadata for a specific book.
   - Example Response:
     ```json
     {
         "Book ID": "Example Book",
         "Book Folder Name": "http://example.com/menu",
         "Chapter": ["Chapter 1", "Chapter 2..."]
     }
     ```

3. **`GET /booksMenu/<book_id>/chapter/<chapter_number>`**
   - Returns content for a specific chapter.
   - Example Response:
     ```json
     {
         "Title": "Chapter 1",
         "Paragraph": [
             "First line of the chapter.",
             "Second line of the chapter."
         ]
     }
     ```

##### How to Run the Server

1. Navigate to the folder containing the Flask server script.
2. Run the server:
   ```bash
   python app.py
   ```
3. Access the endpoints via `http://127.0.0.1:5000`.

##### Example Requests

- Fetch all books:
  ```bash
  curl http://127.0.0.1:5000/booksMenu
  ```

- Fetch metadata for a book:
  ```bash
  curl http://127.0.0.1:5000/booksMenu/1
  ```

- Fetch chapter content:
  ```bash
  curl http://127.0.0.1:5000/booksMenu/1/chapter/1
  ```

---

### Notes

- Ensure the `Books` and `JSON` directories are populated before running the Flask server.
- The API assumes that the folder and file structure matches the output of the novel content scraper.



## Frontend - React Frontend for Novel Reader

This project is a React-based frontend for a novel reading application. It interacts with a Flask backend API to display a list of novels, chapters, and individual pages with customizable settings for user experience. The application supports features such as navigation between chapters, font and background customization.

### Features

#### Core Functionality
- **Home Page**: Displays the list of books fetched from the backend API.
- **Book Menu**: Lists all chapters available for a selected book.
- **Chapter Navigation**: Allows users to navigate through chapters and read their content.

#### Customization Options
- **Background Color**: Users can switch between three background colors: white, black, and grey.
- **Font Color**: Users can toggle between three font colors: white, black, and grey.
- **Font Size**: Users can increase or decrease the font size within a range of 1px to 64px.


#### Error Handling
- Displays loading indicators while fetching data.
- Error messages for API failures with the error details.

#### State Management
- Uses React Query for efficient API calls and caching.
- `useState` is used for UI-related states, such as font size and color settings.

#### Routing
- Implements client-side routing with React Router for seamless navigation.
- Supports routes for home, book menu, and individual chapters.

### Project Structure

```
src/
|└── component/
|   |└── Home/
|   |   └── Home.jsx
|   |└── Book/
|   |   └── Book.jsx
|   |└── Page/
|   |   └── Page.jsx
|   |└── HeadBar/
|   |   └── HeadBar.jsx
|   |└── Footer/
|       └── Footer.jsx
|└── App.css
|└── App.jsx
|└── index.js
```

### Dependencies

#### Core Libraries
- **React**: For building user interfaces.
- **React Router**: For client-side routing.
- **React Query**: For API data fetching and state management.

#### Additional Tools
- **Font Awesome**: For using icons in UI components.

#### Development Environment
- **Node.js**: Required to run the development server.

### API Endpoints

#### Home Page
- **Endpoint**: `GET /booksMenu`
- **Description**: Fetches a list of books with their metadata.

#### Book Menu
- **Endpoint**: `GET /booksMenu/:bookID`
- **Description**: Fetches chapter details for a specific book.

#### Chapter Content
- **Endpoint**: `GET /booksMenu/:bookID/chapter/:chapterID`
- **Description**: Fetches content for a specific chapter.

### How to Run

#### Prerequisites
- Ensure Node.js is installed on your system.
- Backend API should be running locally on `http://127.0.0.1:5000`.

#### Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies:
   ```bash
   npm install
   ```

#### Running the Application
1. Start the development server:
   ```bash
   npm run dev
   ```
2. Open your browser and navigate to `http://localhost:3000`.

## Customization Options

#### Change Background and Font Colors
- Accessible via the HeadBar component.
- Click on the corresponding color icons to update the settings.

#### Adjust Font Size
- Use the `+` and `-` buttons in the HeadBar to increase or decrease font size.

### Known Issues and Limitations
- **CSS Selector Dependency**: Frontend assumes consistent CSS selectors from the backend data.
- **Hardcoded API URL**: Backend URL is hardcoded; make sure it matches your backend server.

### License
This project is open-source and free to use under the MIT license.

---
Feel free to explore, modify, and extend the project to suit your requirements!

