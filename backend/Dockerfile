FROM python:3.13.12

WORKDIR /app

# cOPYING Requirements.txt from root.
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

#Copy Backend code.
# Copy the code in THIS folder (main.py, etc.) into /app/backend
COPY . /app/backend
# prompt.md is now inside backend/, so copy it to /app/prompt.md
COPY prompt.md /app/prompt.md

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
