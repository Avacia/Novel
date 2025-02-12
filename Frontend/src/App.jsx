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

  const colorList = {0: "white", 1: "black", 2: "grey"}

  function ChangeBackgroundColor(index){
    setColor(colorList[Number(index)])
  }

  function ChangeFontColor(index){
    setFontColor(colorList[Number(index)])
  }

  function IncreaseFontSize(){
    setFontSize(Math.min(fontSize + 1, 64))
  }

  function DecreaseFontSize(){
    setFontSize(Math.max(fontSize - 1, 1))
  }


  return(
    <div className="app" style={{backgroundColor: `${color}`, 
        color: `${fontColor}`, fontSize: `${fontSize}px`}}>
      <div className="headBar">
        <HeadBar 
          color={color} 
          setColor={setColor}
          fontColor={fontColor}
          setFontColor={setFontColor}
          fontSize={fontSize}
          setFontSize={setFontSize}
        />
      </div>

      <div className="content">
        <Routes>
          <Route path='/' element={<Home />}></Route>
          <Route path='/addBook' element={<AddBook />}></Route>
          <Route path='/BookMenu/:bookID' element={<Book />}></Route>     
          <Route path='/BookMenu/:bookID/Chapter/:chapterID' element={<Page />}></Route>         
        </Routes>
      </div>

      <div className="footer">
        <Footer />
      </div>
    </div>
  )
}

export default App