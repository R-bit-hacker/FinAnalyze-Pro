# 1. Base Image
FROM python:3.9-slim

# 2. Working Directory set karna
WORKDIR /app

# 3. Pehle requirements copy karo (Caching ke liye best practice)
COPY requirements.txt .

# 4. Dependencies install karo
RUN pip install --no-cache-dir -r requirements.txt

# 5. Sara code copy karo
COPY . .

# 6. Streamlit ka port expose karo
EXPOSE 8501

# 7. App chalane ki command (Email/Database environment variables ke sath)
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]