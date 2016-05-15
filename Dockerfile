FROM python:2.7
RUN pip install --upgrade pip
COPY . /src
WORKDIR /src
RUN pip install --upgrade .
RUN /src/idncheck/idncheck.py example.com
ENTRYPOINT ["/src/idncheck/idncheck.py"]
