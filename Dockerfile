FROM python:3.7-alpine

# docker volume create --name data-generartor-usernames
# docker build -t app-generator .
# docker run -it --rm -v data-generartor-usernames:/usr/src/app:rw app-generator



WORKDIR /usr/src/app

COPY requirements.txt ./
COPY logger.py ./
COPY username.py ./
COPY generator.py ./

RUN pip install -r requirements.txt

RUN mkdir ./output

CMD [ "python", "./generator.py", "-f", "juan antonio", "-l", "flores caba", "-o", "output/test.lst", "-v"]
