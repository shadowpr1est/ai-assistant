import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Note(BaseModel):
    
    heading: str = Field(..., example="Mean Value Theorem")
    summary: str = Field(..., max_length=150)
    page_ref: int | None = Field(None, description="Page number in source PDF")

system = (
    "You are a study summarizer. "
    "Return exactly 10 unique notes that will help prepare for the exam. "
    "Respond *only* with valid JSON matching the Note[] schema."
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": system}],
    response_format={"type": "json_object"}
)

data = json.loads(response.choices[0].message.content)

notes = [ Note(
        
        heading=item["title"],
        summary=item["content"]
    ) for item in data["notes"]]

with open("exam_notes.json", "w") as f:
    json.dump([note.dict() for note in notes], f, indent=2)
print("✅ Notes saved to exam_notes.json")