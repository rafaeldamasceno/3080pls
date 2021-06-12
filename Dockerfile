FROM python:3.7-alpine

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ['python', '3080pls.py']