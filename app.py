import os
import sys
import time
import logging
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

sys.path.append(os.path.dirname(__file__))

from agents.data_agent import data_agent
from utils.database import DatabaseUtil

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AgenticAIDataAgent")

app = FastAPI(
    title="Agentic AI Data Agent REST API",
    description="Production-grade REST backend for multi-agent SQL analytics, ETL pipelines, and data visualization.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks_db = {}


class QueryRequest(BaseModel):
    prompt: str = Field(..., description="Natural language user query")


class TaskResponse(BaseModel):
    task_id: str
    status: str
    route_chosen: str
    result: str
    latency_seconds: float


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Agentic AI Data Agent"}


@app.post("/api/v1/tasks", response_model=TaskResponse)
def submit_task(request: QueryRequest):
    task_id = str(uuid4())
    logger.info(f"Task {task_id} received prompt: {request.prompt}")

    start_time = time.time()
    try:
        response = data_agent.invoke({
            "messages": [HumanMessage(content=request.prompt)],
            "route_response": ""
        })
        latency = round(time.time() - start_time, 3)

        messages = response.get("messages", [])
        last_msg = messages[-1] if messages else ""
        result_text = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        route_chosen = response.get("route_response", "unknown")

        task_data = {
            "task_id": task_id,
            "status": "COMPLETED",
            "route_chosen": route_chosen,
            "result": result_text,
            "latency_seconds": latency
        }
        tasks_db[task_id] = task_data
        logger.info(f"Task {task_id} completed successfully in {latency}s via route {route_chosen}")
        return task_data
    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tasks/{task_id}", response_model=TaskResponse)
def get_task_status(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]


@app.get("/api/v1/schema")
def get_schema():
    conn_details = {
        "host": os.environ.get('host', 'localhost'),
        "port": os.environ.get('port', 5432),
        "user": os.environ.get('user', 'postgres'),
        "password": os.environ.get('password', 'postgres'),
        "dbname": os.environ.get('database', 'postgres')
    }
    db = DatabaseUtil(conn_details)
    return {"schema_info": db.schema_details("public")}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
