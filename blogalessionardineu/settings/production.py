from .base import *
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')



DEBUG = False

ALLOWED_HOSTS= ['194.233.171.61', "blog.alessionardin.eu"]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ['https://blog.alessionardin.eu']


try:
    from .local import *
except ImportError:
    pass
