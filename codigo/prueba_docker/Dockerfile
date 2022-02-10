# Dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
        
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development

CMD ["sh", "-c", "ls; pwd; python3 ./paginaSIS.py & (cd app && flask run)"]
#CMD ["ls", "&&", "python3", "paginaSIS.py", "&"]
#, "(", "cd", "app", "&&", "flask", "run", ")"]
