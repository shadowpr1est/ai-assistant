import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

print("🚀 Starting bootstrap...")
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("🔑 API key loaded")

# 1. Загружаем файл
pdf_path = "data/hollywood.pdf"
with open(pdf_path, "rb") as f:
    file = client.files.create(file=f, purpose="assistants")
print("📄 File uploaded:", file.id)

# 2. Ждём, пока файл будет обработан
print("⏳ Waiting for file to be processed...")
while True:
    file_status = client.files.retrieve(file.id)
    if file_status.status == "processed":
        print("✅ File is processed and ready.")
        break
    elif file_status.status == "failed":
        raise RuntimeError("❌ File processing failed.")
    time.sleep(1)

# 3. Создаём vector store и добавляем файл
vector_store = client.vector_stores.create(name="study_docs")
print("📦 Vector store created:", vector_store.id)

client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id
)
print("📄 File added to vector store.")

# 4. Создаём ассистента
assistant = client.beta.assistants.create(
    name="Study Q&A Assistant",
    instructions=(
        "You are a helpful AI tutor specializing in calculus. "
        "You have access to the textbook 'Calculus Basics'. "
        "Use only the information from that file to answer questions and cite it where appropriate."
    ),
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {
            "vector_store_ids": [vector_store.id]
        }
    }
)
print("✅ Assistant created and linked to vector store:", assistant.id)

# 5. Сохраняем информацию
assistant_info = {
    "assistant_id": assistant.id,
    "vector_store_id": vector_store.id,
    "file_id": file.id,
    "pdf_path": pdf_path
}

with open("assistant_info.json", "w") as f:
    json.dump(assistant_info, f, indent=2)

print("💾 Assistant info saved to assistant_info.json")
