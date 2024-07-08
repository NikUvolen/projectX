from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

dotenv_path = path.join(path.dirname(__file__), '.env')
print(dotenv_path)

if not path.exists(dotenv_path):
    raise FileNotFoundError('.env file not exist')

secret_key = getenv('SECRET_KEY')
email_host_user = getenv('EMAIL_HOST_USER')
email_host_password = getenv('EMAIL_HOST_PASSWORD')
default_from_email = getenv('DEFAULT_FROM_EMAIL')
email_host = getenv('EMAIL_HOST')
email_port = int(getenv('EMAIL_PORT'))
