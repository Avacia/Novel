import { NavLink } from 'react-router-dom'
import { useQuery } from 'react-query'
import { useState } from 'react'
import style from './Home.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlus } from '@fortawesome/free-solid-svg-icons'

export default function Home(){
    const [clicked, setClicked] = useState(false)

    function handleClick(){
        setClicked(!clicked)
    }
    
    async function fetchData(){
        const response = await fetch("http://127.0.0.1:5000/booksMenu")

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        return await response.json()
    }

    
    const { data, isLoading, isError, error } = useQuery("Books", fetchData) 
    console.log("Books data:", data?.books)

    if(isLoading) return <div>Loading......</div>

    if(isError) return <div>Error: {error.message}</div>

    return(
        <div className={style.homeContainer}>
            {data.books.map((book, index) => (
                <div key={index} className={style.book}>
                    <NavLink to={`/BookMenu/${index + 1}`}><p>{book.book_name}</p></NavLink>
                </div>
            ))}
            {!clicked && (
                <NavLink to="/AddBook" className={style.addBookBtn}>
                    <FontAwesomeIcon icon={faPlus} />
                    <p>Add Book</p>
                </NavLink>
            )}
        </div>
    )
}