from pydantic import BaseModel,field_validator

class QuestionRequest(BaseModel):
    query: str

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        if len(v) > 1000:
            raise ValueError("Query is too long (max 1000 characters)")
        return v.strip()

