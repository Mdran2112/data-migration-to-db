import os

CSV_DIRECTORY_PATH = os.getenv("CSV_DIRECTORY_PATH", "/app/historic")
BACKUP_DIRECTORY_PATH = os.getenv("BACKUP_DIRECTORY_PATH", "/app/backup")

API_ADMIN_USER = os.getenv("API_ADMIN_USER", "admin")
API_ADMIN_PASSWORD = os.getenv("API_ADMIN_PASSWORD", "pass")

STAKEHOLDER_USER = os.getenv("STAKEHOLDER_USER", "stakeholder")
STAKEHOLDER_PASSWORD = os.getenv("STAKEHOLDER_PASSWORD", "pass")

HTTP_422_UNPROCESSABLE_ENTITY = 422
