import pandas as pd
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid
import joblib
from model_loader import load_model
from model_routers.stock_news.web_scraper import scrape_web
from model_routers.stock_news.task_manager_functions import run_process
from model_routers.stock_news.nlp import entity_classify

import json
from datetime import datetime

router = APIRouter()

#models = load_model('./saved/diabetes_prediction/models')

def load_tasks_from_file(filename='saved/stock_news/tasks.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except:
        return {}

class ScrapeRequest(BaseModel):
    searchQuery: str
    limit: int

class AnalyseSentimentRequest(BaseModel):
    taskId: str

tasks = load_tasks_from_file()

def save_tasks_to_file(filename='saved/stock_news/tasks.json'):
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)


@router.post('/scrape')
async def scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = { 
        "status": "IN_PROGRESS", 
        "query": request.searchQuery,
        "result": None,
        "urls": [],
        "page_contents": [],
    }
    background_tasks.add_task(
        scrape_web, 
        tasks[task_id], 
        request.searchQuery, 
        request.limit,
        save_tasks_to_file
    )
    return { "taskId": task_id }


@router.get('/scrape_status')
async def scrape_status_all():
    task_list = [{"id": key, **value} for key, value in tasks.items()]
    return sorted(task_list, key=lambda x: datetime.fromisoformat(x['time_started']), reverse=True)[:10]

@router.get('/scrape_status/{task_id}')
async def scrape_status(task_id: str):
    task = tasks.get(task_id)
    if task is None:
        return { "status": "NOT_FOUND" }
    return task

@router.post('/analyse_sentiment')
async def analyse_sentiment(request: AnalyseSentimentRequest):
    if(request.taskId not in tasks):
        return { "result": "INVALID TASK ID" }
    if(tasks[request.taskId]["result"] == None):
        return { "result": "TASK INCOMPLETE" }
    tasks[request.taskId]["sentiment"] = entity_classify(tasks[request.taskId]["result"])
