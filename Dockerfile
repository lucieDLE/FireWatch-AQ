FROM python:3.11-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["gunicorn", "app:server", "--chdir", "app", "-b", "0.0.0.0:7860", "--timeout", "120"]
#  --timeout 120 gives the geopandas startup work headroom on cold build.