    # Установили операйионку и питон
    FROM python:3.8-slim
    # Создаем директорию внутри контейнера
    RUN mkdir /app
    # Копируем с локального компьютера файл зависимостей
    COPY requirements.txt /app
    # Выполнякм установку зависимостей внутри контейнера
    RUN pip3 install -r /app/requirements.txt --no-cache-dir
    # Копируем папку проекта в директорию /app
    COPY api_yamdb/ /app
    # Делаем директорию /app рабочей директорией
    WORKDIR /app
    # Выполняем старт сервера разработки при старте контейнера
    # CMD [ "python3", "manage.py", "runserver", "0:8000" ]
    CMD [ "gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]