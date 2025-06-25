from flask import Flask, render_template
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get DB credentials from .env
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT', 3306))  # default to 3306 if not set

@app.route('/')
def index():
    try:
        # Connect to the MySQL database
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
        connection.close()

        return render_template('table.html', data=result, columns=column_names)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
