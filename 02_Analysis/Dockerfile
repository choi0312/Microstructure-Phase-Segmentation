FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404
WORKDIR /app
COPY requirements.lock.txt .
RUN pip install -r requirements.lock.txt
COPY . .
