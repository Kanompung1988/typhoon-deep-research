"""FastAPI implementation of Typhoon Deep Research backend.

This is a minimal placeholder server showing how the existing
Next.js API routes could be reimplemented in Python. Each endpoint
corresponds to a route in the original project but contains only
stub logic for now.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Typhoon Deep Research Python")


class Learning(BaseModel):
    learning: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None


class ReportRequest(BaseModel):
    prompt: str = Field(..., description="User research query")
    learnings: List[Learning] = Field(default_factory=list)
    language: str = "English"


@app.post("/generate-report")
async def generate_report(req: ReportRequest):
    """Generate a research report.

    In the Next.js application this endpoint called the Typhoon API
    to synthesize research learnings into a markdown report. Here we
    simply echo the request to demonstrate the structure.
    """
    return {
        "prompt": req.prompt,
        "learnings": [learning.model_dump() for learning in req.learnings],
        "language": req.language,
        "report": "Report generation not yet implemented."
    }


class FeedbackRequest(BaseModel):
    feedback: str


@app.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    """Collect user feedback about generated reports."""
    # Placeholder logic; this could store feedback in a database or forward it
    return {"status": "received", "feedback": req.feedback}


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
async def search(req: SearchRequest):
    """Search the web for information about the query.

    The original project used the Tavily API. This stub returns a fixed
    response to show the shape of the data.
    """
    return {
        "query": req.query,
        "results": [
            {"title": "Placeholder result", "url": "https://example.com"}
        ],
    }


@app.post("/process-results")
async def process_results(results: List[dict]):
    """Process raw search results into structured learnings."""
    return {"processed": results}


class QueryGenerationRequest(BaseModel):
    topic: str


@app.post("/generate-queries")
async def generate_queries(req: QueryGenerationRequest):
    """Generate follow-up research queries.

    The Next.js app uses Typhoon to propose clarifying questions. This
    stub returns a single dummy follow-up question.
    """
    return {"queries": [f"What else should we know about {req.topic}?"]}
