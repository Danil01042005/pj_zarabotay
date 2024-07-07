import { useState } from 'react'
import './App.css'
import axios from "axios";

function App() {
    const [vacancies, setVacancies] = useState([]);
    const [filters, setFilters] = useState({
        name: '',
        currency: '',
        region: '',
        salary_from: '',
        salary_to: ''
    });

    // Обработчик изменений в полях ввода
    const handleChange = (event) => {
        const { name, value } = event.target;
        setFilters(prevFilters => ({
            ...prevFilters,
            [name]: value
        }));
    };

    const fetchVacancies = async () => {
        try {
            const response = await axios.get('http://localhost:8000/vacancies/', {
                params: filters
            });
            setVacancies(response.data);
        } catch (error) {
            console.error('Error fetching vacancies:', error);
        }
    };

    return (
        <div className="App">
            <h1>Vacancies</h1>
            <input 
                type="text" 
                name="name" 
                value={filters.name} 
                onChange={handleChange} 
                placeholder="Название вакансии"
            />
            <input 
                type="text" 
                name="currency" 
                value={filters.currency} 
                onChange={handleChange} 
                placeholder="Валюта"
            />
            <input 
                type="text" 
                name="region" 
                value={filters.region} 
                onChange={handleChange} 
                placeholder="Регион"
            />
            <input 
                type="number" 
                name="salary_from" 
                value={filters.salary_from} 
                onChange={handleChange} 
                placeholder="Минимальная зарплата"
            />
            <input 
                type="number" 
                name="salary_to" 
                value={filters.salary_to} 
                onChange={handleChange} 
                placeholder="Максимальная зарплата"
            />
            <button onClick={fetchVacancies}>Клик</button>
            <ul>
                {vacancies.map(vacancy => (
                    <li key={vacancy.id}>{vacancy.name} - {vacancy.salary_from} {vacancy.salary_currency}</li>
                ))}
            </ul>
        </div>
    );
}

export default App
