import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assistant_id = input("Enter assistant ID to delete: ")
client.beta.assistants.delete(assistant_id)
print("🧹 Assistant deleted.")