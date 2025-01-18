FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8050
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:server"]
