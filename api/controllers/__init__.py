import sys

sys.path.append("controllers")
sys.path.append("/app/api/controllers")

from flask_httpauth import HTTPBasicAuth
from globals import USER, PASSWORD

auth = HTTPBasicAuth()

users = {
    USER: PASSWORD
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username) == password
    return False
