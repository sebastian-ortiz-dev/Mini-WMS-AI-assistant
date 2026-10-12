import os
from dotenv import load_dotenv
load_dotenv()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in os.getenv('ALLOWED_EXTENSIONS')