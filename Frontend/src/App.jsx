import './App.css'
import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSquare, faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'

import Home from "./component/Home/Home"
import HeadBar from "./component/HeadBar/Headbar"
import Book from "./component/Book/Book"
import Page from "./component/Page/Page"
import Footer from "./component/Footer/Footer"


function App() {
  const [color, setColor] = useState("white")
  const [fontColor, setFontColor] = useState("black")
  const [fontSize, setFontSize] = useState(16)

  const colorList = {0: "white", 1: "black", 2: "grey"}

  function ChangeBackgroundColor(index){
    setColor(colorList[index])
  }

  function ChangeFontColor(index){
    setFontColor(colorList[index])
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
        <HeadBar />

        <div className="backgroundColor">
          {
            Object.keys(colorList).map((index) => (
              <div key={index} className="colorType">
                <FontAwesomeIcon icon={faSquare} style={{color: `${colorList[index]}`}} onClick={() => ChangeBackgroundColor(index)}/>
              </div>
            ))
          }
        </div>

        <div className="fontColor">
          {
            Object.keys(colorList).map((index) => (
              <div key={index} className="colorType">
                <FontAwesomeIcon icon={faSquare} 
                                 style={{color: `${colorList[index]}`}} 
                                 onClick={() => ChangeFontColor(index)}/>
              </div>
            ))
          }
        </div>

        <div className="fontSize">
          <FontAwesomeIcon icon={faMinus} onClick={DecreaseFontSize}/>
          <p>{fontSize}</p>
          <FontAwesomeIcon icon={faPlus} onClick={IncreaseFontSize}/>
        </div>
      </div>

      <div className="content">
        <Routes>
          <Route path='/' element={<Home />}></Route>
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
