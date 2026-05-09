from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load SHL catalog
try:
    df = pd.read_csv("shl_catalog.csv")
except:
    df = pd.DataFrame(columns=["name", "url"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/")
def home():
    return {"message": "SHL AI Assessment API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Retrieval function
def retrieve_assessments(query):

    query = query.lower()

    recommendations = []

    keywords = {
        "java": "Java",
        "python": "Python",
        "developer": "Developer",
        "manager": "Management",
        "personality": "OPQ",
        "cognitive": "Verify",
        "leadership": "Leadership"
    }

    for key, value in keywords.items():

        if key in query:

            filtered = df[df["name"].str.contains(value, case=False, na=False)]

            for _, row in filtered.head(5).iterrows():

                recommendations.append({
                    "name": row["name"],
                    "url": row["url"],
                    "test_type": "K"
                })

    return recommendations[:10]

@app.post("/chat")
def chat(req: ChatRequest):

    if not req.messages:
        return {
            "reply": "Please provide hiring requirements.",
            "recommendations": [],
            "end_of_conversation": False
        }

    last_message = req.messages[-1].content.lower()

    # Clarification support
    if len(last_message.split()) < 3:

        return {
            "reply": "Please specify role, skills, and seniority level.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Comparison support
    if "compare" in last_message or "vs" in last_message:

        return {
            "reply": "OPQ focuses on personality insights while Verify focuses on cognitive abilities and job readiness.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # Refinement support
    if "add" in last_message:

        recommendations = retrieve_assessments(last_message)

        return {
            "reply": "Updated recommendations with additional constraints.",
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    # Retrieval
    recommendations = retrieve_assessments(last_message)

    # No results
    if not recommendations:

        return {
            "reply": "Could not find relevant SHL assessments. Please refine your query.",
            "recommendations": [],
            "end_of_conversation": False
        }

    return {
        "reply": "Here are recommended SHL assessments based on your hiring requirements.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }