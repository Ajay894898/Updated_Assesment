import re
import logging
from transformers import pipeline
from database import get_db_connection

# Logger
logger = logging.getLogger(__name__)

# Summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def fetch_data(user_input):
    """Fetch relevant data based on user input."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    logger.info(f"Received user_input: {user_input}")
    
    try:
        user_input_lower = user_input.lower()
        # ✅ Brand-based query
        if "brand" in user_input_lower or "products" in user_input_lower:
            words = user_input_lower.split()
            possible_brands = ["apple", "samsung", "dell"]  # Expand as needed
            brand = next((word for word in words if word in possible_brands), None)

            if brand:
                logger.info(f"Extracted brand: {brand}")
                cursor.execute("SELECT * FROM products WHERE LOWER(brand) = %s", (brand,))
            else:
                logger.error("Brand not recognized in query")
                return {"data": [], "error": "Brand not recognized"}

        # ✅ Supplier-based query
        elif "suppliers" in user_input_lower:
            match = re.search(r'provide (.+)', user_input_lower)
            category = match.group(1).strip() if match else None

            if category:
                logger.info(f"Extracted category: {category}")
                cursor.execute("SELECT * FROM suppliers WHERE LOWER(product_categories_offered) LIKE %s", ('%' + category + '%',))
            else:
                logger.error("Category extraction failed")
                return {"data": [], "error": "Invalid query format"}

        # ✅ Product category query (like "Give me all laptops")
        elif "laptop" in user_input_lower or "tablet" in user_input_lower or "phone" in user_input_lower:
            category = "laptop" if "laptop" in user_input_lower else ("tablet" if "tablet" in user_input_lower else "phone")
            logger.info(f"Extracted category: {category}")
            cursor.execute("SELECT * FROM products WHERE LOWER(category) = %s", (category,))
        
        # ✅ Product details query
        elif "details" in user_input_lower:
            match = re.search(r'details of (.+)', user_input_lower)
            product_name = match.group(1).strip() if match else None

            if product_name:
                product_name = product_name.replace("product", "").strip()
                logger.info(f"Extracted product name: {product_name}")
                cursor.execute("SELECT * FROM products WHERE LOWER(name) LIKE %s", ('%' + product_name + '%',))
            else:
                logger.error("Product name extraction failed")
                return {"data": [], "error": "Invalid query format. Please try again"}
        
        else:
            logger.error("Please give right instructions")
            return {"data": [], "error": "Please give right instructions"}

        results = cursor.fetchall()
        logger.info(f"Fetched data: {results}")
        return {"data": results}

    except Exception as e:
        logger.error(f"Database query error: {e}")
        return {"data": [], "error": str(e)}

    finally:
        cursor.close()
        conn.close()

def summarize_data(data):
    """Summarizes the fetched query results."""
    if not data:
        return "No relevant data found."

    summary = []
    for item in data:
        if "brand" in item:  # ✅ For products
            summary.append(f"Product: {item['name']}, Brand: {item['brand']}, Price: ${item['price']}, Category: {item['category']}, Description: {item['description']}")
        else:  # ✅ For suppliers
            summary.append(f"Supplier: {item['name']}, Contact: {item['contact_info']}, Categories: {item['product_categories_offered']}")

    return "\n".join(summary)

def execute_workflow(user_input):
    """Processes user input and returns summarized details."""
    try:
        fetch_result = fetch_data(user_input)

        if not fetch_result["data"]:  # ✅ If no data, return a friendly message
            return {"response": fetch_result.get("error", "No relevant data found.")}

        summary = summarize_data(fetch_result["data"])
        return {"response": summary}

    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}
