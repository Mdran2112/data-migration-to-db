import sys

sys.path.append("controllers")
sys.path.append("/app/api/controllers")

from flask_httpauth import HTTPBasicAuth
from globals import API_ADMIN_USER, API_ADMIN_PASSWORD, STAKEHOLDER_USER, STAKEHOLDER_PASSWORD

admin_auth = HTTPBasicAuth()
stakeholder_auth = HTTPBasicAuth()

admin_users = {
    API_ADMIN_USER: API_ADMIN_PASSWORD
}

stakeholder_user = {
    STAKEHOLDER_USER: STAKEHOLDER_PASSWORD
}


def verify_pass(username, password, user_pass_dict) -> bool:
    if username in user_pass_dict:
        return user_pass_dict.get(username) == password
    return False


@admin_auth.verify_password
def verify_password_admin(username, password):
    return verify_pass(username, password, admin_users)


@stakeholder_auth.verify_password
def verify_password_stkholder(username, password):
    return verify_pass(username, password, stakeholder_user)
