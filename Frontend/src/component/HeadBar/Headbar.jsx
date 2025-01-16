import { NavLink, useLocation } from "react-router-dom"
import { useState, useEffect } from 'react'
import style from './HeadBar.module.css'

export default function HeadBar(){
    const location = useLocation()
    const [isHomePage, setIsHomePage] = useState(true)
    const [isBookMenu, setIsBookMenu] = useState(false)

    useEffect(() => {
        setIsHomePage(location.pathname === "/")
        setIsBookMenu(location.pathname.startsWith('/BookMenu/') 
                      && location.pathname.includes('/Chapter'))
    }, [location.pathname])

    
    function getMenuLocation(path){
        return path.split("/Chapter")[0]
    }

    return(
        <div className={style.headBarContainer}>
            <NavLink to='/' className={style.headBarLink}>Home</NavLink>
            {
                !isHomePage && isBookMenu &&
                <NavLink to={getMenuLocation(location.pathname)} className={style.headBarLink}>
                            Book Menu
                </NavLink>
            }
        </div>
    )
}