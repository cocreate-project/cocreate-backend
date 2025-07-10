import os
from dotenv import load_dotenv
from cocreate import create_app
from cocreate.utils import db, log
from flask_cors import CORS

load_dotenv()

app = create_app()
CORS(app)

log.generate()

if __name__ == "__main__":
    db.create_database()
    port = int(os.getenv("PORT", 5000))
    app.run(port=port)
