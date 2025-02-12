# Novel Reader

A modern web application for reading novels with customizable reading experience and content management system.

## Core Features

### Reading Experience
- Responsive grid layout displaying all books
- Customizable interface:
  - Dynamic font size control (1-64px) with manual input
  - Background color selection (white, black, grey)
  - Font color selection (white, black, grey)
- Clean navigation system between books and chapters
- Modern, minimalist design with consistent styling

### Book Management
- Add new books through an intuitive form interface
- Configure scraping parameters:
  - Book name and menu URL
  - CSS selectors for content extraction
  - Multi-page support
  - Unwanted content filtering
- Organized chapter navigation

### Content Processing
- Automated novel content scraping
- Concurrent chapter processing
- Structured data storage
- Error handling and validation

## Technical Stack

### Frontend
- React with Vite
- State Management: React Query
- Routing: React Router DOM
- Styling: CSS Modules
- Icons: FontAwesome
- HTTP Client: Fetch API

### Backend
- Python Flask REST API
- BeautifulSoup4 for web scraping
- Concurrent.futures for parallel processing
- JSON-based data storage

## API Endpoints

### Books
- GET `/booksMenu` - Retrieve all books
- GET `/booksMenu/:bookId` - Get specific book details
- GET `/booksMenu/:bookId/chapter/:chapterId` - Fetch chapter content
- POST `/addBooks` - Add new book with scraping configuration

## Project Structure
```bash
├── Frontend/
│   ├── src/
│   │   ├── component/
│   │   │   ├── AddBook/
│   │   │   ├── Book/
│   │   │   ├── Footer/
│   │   │   ├── HeadBar/
│   │   │   ├── Home/
│   │   │   └── Page/
│   │   └── App.jsx
│   
└── Backend/
    ├── server.py
    ├── novelLibrary.py
    ├── novelScrapper.py
    └── getNovelContent.py
```


## Setup Instructions

### Frontend Development
```bash
cd Frontend
npm install
npm run dev
```

### Backend Development
```bash
cd Backend
pip install -r requirements.txt
python server.py
```

## Data Storage
- Books stored in JSON format
- Structured chapter organization
- Metadata management for scraping configuration

## Design System
- Consistent spacing using viewport units
- Responsive grid layouts
- Modern shadow effects
- Smooth transitions and hover states
- Error state handling with visual feedback

This README provides a clear overview of your project's architecture, features, and setup process while maintaining the modern, clean aesthetic present in your codebase.