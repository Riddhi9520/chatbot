import os
import google.generativeai as genai
import mysql.connector

# Function to Connect to MySQL Database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",        # Change if needed
        user="root",             # Your MySQL username
        password="root", # Your MySQL password
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

genai.configure(api_key="AIzaSyAYlRenvT1Q99YEZdBHjko48Riz29jPb7U")

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
#dummy prompts
def GenerateResponse(input_text):
   response = model.generate_content([
  "you are a whatsApp chatbot, so reply accordingly",
  "input: who are you",
  "output: I am a WhatsApp Assistant",
  "input: what all can you do?",
  "output: I can help u with resolving any issue that you might be facing while using WhatsApp! How can i help?",
  "input: can u generate images?",
  "output:no, I can't generate images but I can help you with any issue that you might be facing while using WhatsApp! How can i help?",
  "input: can u generate text?",
  "output: yes, I can generate text!",
  f"input: {input_text}",
  "output: ",
  ])

   return response.text
 
# while True:
#       string = str(input("Enter the prompt: "))
#       print("Bot: ",GenerateResponse(string))