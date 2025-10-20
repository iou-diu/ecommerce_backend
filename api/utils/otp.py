import random
import string

def generate_random_otp_code(length=6):
    characters = '1234567890'
    return ''.join(random.choice(characters) for _ in range(length))

# def generate_random_otp_code(length=6):
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))