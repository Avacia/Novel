import './App.css'
import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'

import Home from "./component/Home/Home"
import HeadBar from "./component/HeadBar/Headbar"
import Book from "./component/Book/Book"
import AddBook from "./component/AddBook/AddBook"
import Page from "./component/Page/Page"
import Footer from "./component/Footer/Footer"

function App() {
  const [color, setColor] = useState("white")
  const [fontColor, setFontColor] = useState("black")
  const [fontSize, setFontSize] = useState(16)

  return (
    <div 
      className="app" 
      style={{
        backgroundColor: color,
        color: fontColor, 
        fontSize: `${fontSize}px`
      }}
    >
      <HeadBar 
        color={color} 
        setColor={setColor}
        fontColor={fontColor}
        setFontColor={setFontColor}
        fontSize={fontSize}
        setFontSize={setFontSize}
      />

      <main className="content">
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/addBook' element={<AddBook />} />
          <Route path='/BookMenu/:bookID' element={<Book />} />     
          <Route path='/BookMenu/:bookID/Chapter/:chapterID' element={<Page />} />         
        </Routes>
      </main>

      <Footer />
    </div>
  )
}

export default App
