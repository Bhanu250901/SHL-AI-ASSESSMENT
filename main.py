from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

df = pd.read_csv("shl_catalog.csv")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    last_message = req.messages[-1].content.lower()

    recommendations = []

    keywords = {
        "java": "Java",
        "python": "Python",
        "personality": "OPQ",
        "developer": "Developer",
        "manager": "Management"
    }

    matched = False

    for key, value in keywords.items():

        if key in last_message:

            matched = True

            filtered = df[df["name"].str.contains(value, case=False, na=False)]

            for _, row in filtered.head(5).iterrows():

                recommendations.append({
                    "name": row["name"],
                    "url": row["url"],
                    "test_type": "K"
                })

    if matched and recommendations:

        return {
            "reply": "Here are recommended SHL assessments.",
            "recommendations": recommendations[:10],
            "end_of_conversation": True
        }

    return {
        "reply": "Please tell me role, skills, and experience level.",
        "recommendations": [],
        "end_of_conversation": False
    }