from pydantic import BaseModel,Field

class QuestionRequest(BaseModel):
   query : str
