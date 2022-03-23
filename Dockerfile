FROM python:3.9
WORKDIR /steesh/backend
COPY requirements.txt .
RUN pip3 install --upgrade pip -r requirements.txt
COPY . .
RUN apt-get update && apt-get install -y \
    wkhtmltopdf
EXPOSE 5000
