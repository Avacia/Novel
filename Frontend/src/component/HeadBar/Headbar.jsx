import { NavLink, useLocation } from "react-router-dom"
import { useState, useEffect } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import style from './HeadBar.module.css'

export default function HeadBar({ color, setColor, fontColor, setFontColor, fontSize, setFontSize }){
    const location = useLocation()
    const [isHomePage, setIsHomePage] = useState(true)
    const [isBookMenu, setIsBookMenu] = useState(false)
    const colorList = ["white", "black", "grey"]

    useEffect(() => {
        setIsHomePage(location.pathname === "/")
        setIsBookMenu(location.pathname.startsWith('/BookMenu/') 
                      && location.pathname.includes('/Chapter'))
    }, [location.pathname])

    function getMenuLocation(path){
        return path.split("/Chapter")[0]
    }

    function handleFontSizeChange(e) {
        const value = parseInt(e.target.value)
        if (!isNaN(value)) {
            setFontSize(Math.min(Math.max(value, 1), 64))
        }
    }

    return(
        <nav className={style.headBarContainer}>
            <div className={style.navigation}>
                <NavLink to='/' className={style.headBarLink}>
                    <span>Home</span>
                </NavLink>
                {!isHomePage && isBookMenu && (
                    <NavLink to={getMenuLocation(location.pathname)} className={style.headBarLink}>
                        <span>Book Menu</span>
                    </NavLink>
                )}
            </div>
            <div className={style.controls}>
                <div className={style.colorControl}>
                    <label>Background</label>
                    <select 
                        className={style.colorSelect} 
                        value={color}
                        onChange={(e) => setColor(e.target.value)}
                    >
                        {colorList.map((color) => (
                            <option key={color} value={color}>
                                {color}
                            </option>
                        ))}
                    </select>
                </div>
                <div className={style.colorControl}>
                    <label>Font</label>
                    <select 
                        className={style.colorSelect}
                        value={fontColor}
                        onChange={(e) => setFontColor(e.target.value)}
                    >
                        {colorList.map((color) => (
                            <option key={color} value={color}>
                                {color}
                            </option>
                        ))}
                    </select>
                </div>
                <div className={style.fontSize}>
                    <FontAwesomeIcon icon={faMinus} onClick={() => setFontSize(Math.max(fontSize - 1, 1))}/>
                    <input 
                        type="number" 
                        value={fontSize}
                        onChange={handleFontSizeChange}
                        min="1"
                        max="64"
                    />
                    <FontAwesomeIcon icon={faPlus} onClick={() => setFontSize(Math.min(fontSize + 1, 64))}/>
                </div>
            </div>
        </nav>
    )
}
