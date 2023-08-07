FROM python:3.11
WORKDIR /steesh/backend
COPY requirements.txt .
RUN pip3 install --upgrade pip -r requirements.txt
COPY . .
EXPOSE 8000
