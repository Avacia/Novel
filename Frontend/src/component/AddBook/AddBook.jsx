import style from './AddBook.module.css'
import { useState } from 'react'
import { useNavigate, NavLink } from 'react-router-dom'
import { useQueryClient } from 'react-query'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronLeft, faCheck, faRotateLeft } from '@fortawesome/free-solid-svg-icons'

export default function AddBook() {
    const navigate = useNavigate()
    const queryClient = useQueryClient()

    const [formData, setFormData] = useState({
        bookName: '',
        menuURL: '',
        multiPageLink: '',
        pageCSS: '',
        pageLink: '',
        titleCSS: '',
        bodyCSS: '',
        unwanted: ''
    })
    const [errors, setErrors] = useState({})

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }))
        }
    }

    const validateForm = () => {
        const requiredFields = ['bookName', 'menuURL', 'pageCSS', 'pageLink', 'titleCSS', 'bodyCSS']
        const newErrors = {}
        
        requiredFields.forEach(field => {
            if (!formData[field].trim()) {
                newErrors[field] = 'This field is required'
            }
        })

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async () => {
        if (!validateForm()) return

        try {
            const response = await fetch('http://127.0.0.1:5000/addBooks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })

            if (!response.ok) throw new Error('Failed to add book')
            
            handleReset()
            queryClient.invalidateQueries('Books')
            navigate('/')
        } catch (error) {
            alert('Error adding book:', error)
        }
    }

    const handleReset = () => {
        setFormData(prev => Object.fromEntries(
            Object.keys(prev).map(key => [key, ''])
        ))
        setErrors({})
    }

    const inputFields = [
        { name: 'bookName', label: 'Book Name*', placeholder: 'Book Name' },
        { name: 'menuURL', label: 'Menu URL*', placeholder: 'Menu URL' },
        { name: 'multiPageLink', label: 'Multi Page CSS', placeholder: 'Multi Page CSS' },
        { name: 'pageCSS', label: 'Page CSS*', placeholder: 'Page CSS' },
        { name: 'pageLink', label: 'Page Link*', placeholder: 'Page Link' },
        { name: 'titleCSS', label: 'Title CSS*', placeholder: 'Title CSS' },
        { name: 'bodyCSS', label: 'Body CSS*', placeholder: 'Body CSS' },
        { name: 'unwanted', label: 'Unwanted CSS', placeholder: 'Unwanted CSS' }
    ]

    return (
        <div className={style.addBookContainer}>
            <div className={style.heading}>
                <NavLink to="/" className={style.backButton}>
                    <FontAwesomeIcon icon={faChevronLeft} />
                    <span>Back to Home</span>
                </NavLink>
                <h1>Add New Book</h1>
            </div>
            <div className={style.formContainer}>
                {inputFields.map(({ name, label, placeholder }) => (
                    <div key={name} className={style.inputGroup}>
                        <label>{label}</label>
                        <div className={style.inputWrapper}>
                            <input
                                type="text"
                                name={name}
                                placeholder={placeholder}
                                value={formData[name]}
                                onChange={handleChange}
                                className={errors[name] ? style.errorInput : ''}
                            />
                            {errors[name] && <span className={style.errorText}>{errors[name]}</span>}
                        </div>
                    </div>
                ))}
                <div className={style.btnContainer}>
                    <button className={style.submitBtn} onClick={handleSubmit}>
                        <FontAwesomeIcon icon={faCheck} />
                        <span>Submit</span>
                    </button>
                    <button className={style.resetBtn} onClick={handleReset}>
                        <FontAwesomeIcon icon={faRotateLeft} />
                        <span>Reset</span>
                    </button>
                </div>
            </div>
        </div>
    )    
}