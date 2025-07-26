import random
import string

def generate_auth_code():
    return str(random.randint(1000, 9999))

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
