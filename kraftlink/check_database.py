import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

def test_db_connection():
    try:
        # Establish the connection
        connection = psycopg2.connect(DATABASE_URL)
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # Execute a simple SQL query
        cursor.execute("SELECT 1;")
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            print("Connection to the database was successful!")
        else:
            print("Failed to execute test query.")

        # Close the cursor and connection
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_db_connection()
