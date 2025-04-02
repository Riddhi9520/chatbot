import os
import google.generativeai as genai
import mysql.connector
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API Key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Configure GenAI with the key
genai.configure(api_key=api_key)

# Function to Connect to MySQL Database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",        # Change if needed
        user="root",             # Your MySQL username
        password="", # Your MySQL password
        database="chatbot"  # Database name
    )
    
    
import mysql.connector

def load_chat_history():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT 'user' AS role, user_message AS content FROM chat_history "
                   "UNION ALL "
                   "SELECT 'assistant' AS role, bot_response AS content FROM chat_history "
                   "ORDER BY role ASC")
    chat_history = cursor.fetchall()
    connection.close()
    return chat_history

def delete_chat_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM chat_history"  # Delete all rows from the chat_history table
        cursor.execute(query)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")
        
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

def GenerateResponse(prompt):
    predefined_responses = {
        "hello": "Hi there! How can I assist you?",
        "hi": "Hello! How can I help you today?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "bye": "Goodbye! Have a great day!",
        "what is your name": "I'm your chatbot, here to help you!",
        "thanks": "You're welcome!"
    }

    # Convert input to lowercase for case-insensitive matching
    prompt_lower = prompt.lower()

    # Check if the input exists in predefined responses
    if prompt_lower in predefined_responses:
        return predefined_responses[prompt_lower]

    # If not found in predefined responses, generate AI-based response
    response = chat_session.send_message(f"Input: {prompt}")

    return response.text  # AI-generated response

