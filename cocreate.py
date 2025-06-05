from dotenv import load_dotenv
from cocreate import create_app
from cocreate.utils import db
from flask_cors import CORS

load_dotenv()

app = create_app()
CORS(app)

if __name__ == "__main__":
    db.create_database()
    app.run()
