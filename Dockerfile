FROM python:3.9
WORKDIR /steesh/backend
RUN apt-get update && apt-get install -y \
    wkhtmltopdf
COPY requirements.txt .
RUN pip3 install --upgrade pip -r requirements.txt
COPY . .
EXPOSE 5000
