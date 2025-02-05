import mariadb
import logging
from fastapi import HTTPException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection setup
def get_db_connection():
    try:
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot"
        )
        logger.info("Database connection established successfully!")
        return conn
    except mariadb.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
