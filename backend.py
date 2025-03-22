import os
import google.generativeai as genai
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

# Function to Connect to MySQL Database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",        # Change if needed
        user="root",             # Your MySQL username
        password="", # Your MySQL password
        database="chatbot"  # Database name
    )

# Function to Save Chat to Database
def save_chat(user_input, bot_response):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO chat_history (user_message, bot_response) VALUES (%s, %s)"
        values = (user_input, bot_response)
        cursor.execute(query, values)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def GenerateResponse(input_text):
  response = chat_session.send_message(f"Input: {input_text}")
  return response.text
