import { useLocation, useParams } from 'react-router-dom'
import { useQuery } from 'react-query'
import { useState } from 'react'
import style from './Page.module.css'

export default function Page(){
    const { bookID, chapterID } = useParams()
    const [currentPage, setCurrentPage] = useState(parseInt(chapterID))
    const { state } = useLocation()
    const chapterLength = state?.chapterLength

    async function fetchChapter(booksID, chaptersID){
        const response = 
            await fetch(`http://127.0.0.1:5000/booksMenu/${booksID}/chapter/${chaptersID}`)

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        return await response.json()
    }
    

    function goPrevious(){
        setCurrentPage(Math.max(currentPage - 1, 1))
    }


    function goNext(){
        setCurrentPage(Math.min(currentPage + 1, chapterLength))
    } 

    const { data, isLoading, isError, error } = 
            useQuery(["Chapter", bookID, currentPage], () => fetchChapter(bookID, currentPage))

    if(isLoading) return <div>Loading......</div>

    if(isError) return <div>Error: {error.message}</div>


    return(
        <div className={style.pageContainer}>
            <h1>{data.Title}</h1>

            <div className={style.contentContainer}>
                {
                    data.Paragraph.map((content, index) => (
                        <p key={index}>{content}</p>
                    ))
                }
            </div>
            
            <div className={style.btnContainer}>
                <button className={style.btn} onClick={goPrevious}>Previous</button>
                <p>Page: {currentPage}</p>
                <button className={style.btn} onClick={goNext}>Next</button>
            </div>
        </div>
    )
}