FROM python
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN python3 obs-test.py
RUN python3 cdn-test.py
CMD ["python3", "cdn-test.py"]
