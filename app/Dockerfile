
FROM python:3.12.2


WORKDIR /usr/src/app


COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000


ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
