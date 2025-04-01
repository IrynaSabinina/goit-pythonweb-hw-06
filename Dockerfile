FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

CMD ["poetry", "run", "python", "main.py"]
