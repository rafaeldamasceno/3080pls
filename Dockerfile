FROM python:3.7-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir log
COPY . .

CMD ["python", "3080pls.py"]