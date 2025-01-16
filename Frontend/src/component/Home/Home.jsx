import { NavLink } from 'react-router-dom'
import { useQuery } from 'react-query'
import style from './Home.module.css'

export default function Home(){
    
    async function fetchData(){
        const response = await fetch("http://127.0.0.1:5000/booksMenu")

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        return await response.json()
    }

    
    const { data, isLoading, isError, error } = useQuery("Books", fetchData) 

    if(isLoading) return <div>Loading......</div>

    if(isError) return <div>Error: {error.message}</div>

    return(
        <div className={style.homeContainer}>
            {
                Object.entries(data.Folders).map((jsonFile, index) => (
                    <div key={index} className={style.book}>
                        <NavLink to={`/BookMenu/${index + 1}`}><p>{jsonFile[1].Name}</p></NavLink>
                    </div>
                ))
            }
        </div>
    )
}