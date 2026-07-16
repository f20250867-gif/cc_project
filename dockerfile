# choosing image to extend
FROM python:3.12.9-slim-bookworm
# not letting byte code files(.pyc) on disk inside docker container and prevent python from buffering output to standard output. useful for log messages immediately appearing in terminal  
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#copying everything into container(app)
COPY . .

EXPOSE 8000
# command to execute 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
