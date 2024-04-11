FROM python
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ["python3", "cdn-test.py"]
