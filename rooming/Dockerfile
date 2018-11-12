FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]
ENTRYPOINT ["sh", "/code/docker-entrypoint.sh"]
EXPOSE 8000
