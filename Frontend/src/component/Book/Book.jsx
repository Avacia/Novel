import { useQuery } from 'react-query'
import { useParams, NavLink } from 'react-router-dom'
import style from './Book.module.css'

export default function Book(){
    const { bookID } = useParams()

    async function getBookData(bookId){
        const response = await fetch(`http://127.0.0.1:5000/booksMenu/${bookId}`)

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        return await response.json()
    }


    const {data, isLoading, isError, error} = useQuery(["Book", bookID], () => getBookData(bookID))

    if(isLoading) return(<div>Loading......</div>)

    if(isError) return(<div>Error: {error.message}</div>)


    return(
        <div className={style.bookContainer}>
            <h1>{data.FolderName}</h1>

            <div className={style.chapterContainer}>
                {
                    Object.entries(data.Chapter).map((chapter, index) => (
                        <div key={index} className={style.chapter}>
                            <NavLink to={`/BookMenu/${bookID}/Chapter/${index + 1}`}
                                     state={{ chapterLength: data.Chapter.length }}>
                                        <p>{chapter[1].split(".json")[0]}</p>
                            </NavLink>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}