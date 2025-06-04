import json
import pytest
from pydantic import BaseModel, Field, ValidationError

class Note(BaseModel):
    id: int = Field(..., ge=1, le=10)
    heading: str
    summary: str = Field(..., max_length=150)
    page_ref: int | None = None

def test_notes_schema():
    with open("exam_notes.json") as f:
        notes = json.load(f)
    for item in notes:
        try:
            Note(**item)
        except ValidationError as e:
            pytest.fail(f"Invalid note: {e}")

print("✅ Schema test ready. Run with: pytest tests/")