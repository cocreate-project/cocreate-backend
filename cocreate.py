from dotenv import load_dotenv
from cocreate import create_app
from cocreate.utils import db, generate_log_file
 
generate_log_file.log_generate()

load_dotenv()

app = create_app()

if __name__ == "__main__":
    db.create_database()
    app.run()