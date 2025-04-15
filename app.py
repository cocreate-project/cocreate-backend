from dotenv import load_dotenv
from cocreate import create_app
from cocreate.utils import db

load_dotenv()

app = create_app()

if __name__ == "__main__":
    db.create_database()
    app.run()
