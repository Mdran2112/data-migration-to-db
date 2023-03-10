import os

CSV_DIRECTORY_PATH = os.getenv("CSV_DIRECTORY_PATH", "/app/historic")

USER = os.getenv("API_USER", "admin")
PASSWORD = os.getenv("API_PASSWORD", "pass")

HTTP_422_UNPROCESSABLE_ENTITY = 422