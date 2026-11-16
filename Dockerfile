FROM mcr.microsoft.com/playwright/python:v1.60.0-noble

WORKDIR /app

COPY requirements-lock.txt ./

RUN python -m pip install --no-cache-dir -r requirements-lock.txt

COPY . .

ENTRYPOINT ["python", "-m", "pytest"]

CMD ["-v"]