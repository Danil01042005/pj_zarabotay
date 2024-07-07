import requests
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from decimal import Decimal
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Конфигурация базы данных
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'  # Замените на ваши данные для подключения

Base = declarative_base()

# Модель для таблицы вакансий
class Vacancy(Base):
    __tablename__ = 'vacancies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    employer = Column(String)
    area = Column(String)
    salary_from = Column(Float)
    salary_to = Column(Float)
    salary_currency = Column(String)
    requirement = Column(Text)
    responsibility = Column(Text)
    url = Column(String)

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# Разрешение CORS для взаимодействия с фронтендом
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic модель для фильтров
class VacancyFilter(BaseModel):
    id: int
    name: Optional[str] = None
    employer: Optional[str] = None
    area: Optional[str] = None
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    salary_currency: Optional[str] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None
    url: Optional[str] = None

# Функция для получения вакансий по заданным параметрам
@app.get("/vacancies/", response_model=List[VacancyFilter])
def get_vacancies(
    name: Optional[str] = None,
    currency: Optional[str] = None,
    region: Optional[str] = None,
    salary_from: Optional[float] = None,
    salary_to: Optional[float] = None
):
    session = Session()
    query = session.query(Vacancy)
    
    if name:
        query = query.filter(Vacancy.name.ilike(f'%{name}%'))
    if currency:
        query = query.filter(Vacancy.salary_currency == currency)
    if region:
        query = query.filter(Vacancy.area == region)
    if salary_from:
        query = query.filter(Vacancy.salary_from >= salary_from)
    if salary_to:
        query = query.filter(Vacancy.salary_to <= salary_to)
    
    vacancies = query.all()
    session.close()
    return vacancies

# Функция для получения вакансий
def fetch_vacancies(params):
    headers = {
        'User-Agent': 'api-test-agent'
    }
    
    url = 'https://api.hh.ru/vacancies'
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)  # Таймаут 10 секунд
        response.raise_for_status()  # Проверка на наличие HTTP ошибок
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP ошибка: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Ошибка соединения: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Ошибка таймаута: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Ошибка запроса: {req_err}")
    return None

# Функция для сохранения данных в базу
def save_vacancies(session, vacancies):
    for item in vacancies.get('items', []):
        title = item.get('name')
        employer = item.get('employer', {}).get('name')
        area = item.get('area', {}).get('name')
        salary = item.get('salary')
        if salary:
            salary_from = Decimal(salary.get('from', 0) or 0)
            salary_to = Decimal(salary.get('to', 0) or 0)
            currency = salary.get('currency')
        else:
            salary_from = None
            salary_to = None
            currency = None

        requirement = item.get('snippet', {}).get('requirement', '')
        responsibility = item.get('snippet', {}).get('responsibility', '')
        url = item.get('alternate_url')

        vacancy = Vacancy(
            name=title,
            employer=employer,
            area=area,
            salary_from=salary_from,
            salary_to=salary_to,
            salary_currency=currency,
            requirement=requirement,
            responsibility=responsibility,
            url=url
        )

        session.add(vacancy)
    session.commit()

# Эндпоинт для получения и сохранения вакансий
@app.post("/fetch-vacancies/")
def fetch_and_save_vacancies(params: dict):
    data = fetch_vacancies(params)
    if not data:
        raise HTTPException(status_code=400, detail="Failed to fetch vacancies")
    
    session = Session()
    save_vacancies(session, data)
    return {"status": "success"}
