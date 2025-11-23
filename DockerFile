FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN useradd -m -u 1000 user

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY api ./api

RUN chown -R user:user /app

USER user

EXPOSE 7860

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "7860"]
