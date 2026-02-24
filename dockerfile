FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN apk add --no-cache bash netcat-openbsd

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir "gunicorn" "uvicorn[standard]"

COPY . .

RUN sed -i 's/\r$//' start_script.sh && chmod +x start_script.sh

EXPOSE 8000

CMD ["bash", "./start_script.sh"]