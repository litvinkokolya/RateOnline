# Используй базовый образ Python
FROM python:3.9

# Устанавливаем переменную окружения для запуска в режиме "продакшн"
ENV PYTHONUNBUFFERED 1

# Создаем директорию для приложения в контейнере
RUN mkdir /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости проекта в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости проекта
RUN pip install -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/