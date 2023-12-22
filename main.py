from fastapi import FastAPI, HTTPException, Body, Path
import requests
import asyncio
import random
from models import Event, GroupModel
from urllib.parse import urlencode
import multiprocessing as mp
import datetime

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EVENT_SERVICE_URL = "http://3.134.34.54:8011"
GROUP_SERVICE_URL = "https://coms6156-f23-sixguys.ue.r.appspot.com"
USER_SERVICE_URL = "http://ec2-44-219-26-13.compute-1.amazonaws.com:8000"

# Health Check Endpoints
@app.get("/check/event-service")
async def check_event_service():
    return await check_service_status(EVENT_SERVICE_URL)

@app.get("/check/group-service")
async def check_group_service():
    return await check_service_status(GROUP_SERVICE_URL)

@app.get("/check/user-service")
async def check_user_service():
    return await check_service_status(USER_SERVICE_URL)

async def check_service_status(service_url, name="service"):
    await asyncio.sleep(random.uniform(0, 1e-3)) 
    try:
        response = requests.get(service_url)
        response.raise_for_status()	
        finish_time = datetime.datetime.now()
        return {f"{name} status": "ONLINE", "time": finish_time}
    except requests.RequestException:
        return {f"{name} status": "OFFLINE"}

# Event Service Endpoints
@app.post("/events/create")
async def create_event(group_id: str, user_id: str, event_data: Event):
    query_params = urlencode({"user_id": user_id})
    response = requests.post(f"{EVENT_SERVICE_URL}/api/{group_id}/events?{query_params}", json=event_data.model_dump())
    return handle_response(response)

@app.get("/events/{event_id}")
async def get_event(event_id: str):
    response = requests.get(f"{EVENT_SERVICE_URL}/api/events/{event_id}")
    return handle_response(response)

@app.put("/events/{event_id}/update_name")
async def update_event(event_id: str, event_name: str):
    query_params = urlencode({"event_name": event_name})
    response = requests.put(f"{EVENT_SERVICE_URL}/api/events/{event_id}/update_name?{query_params}")
    return handle_response(response)

@app.delete("/events/{event_id}")
async def delete_event(event_id: str):
    response = requests.delete(f"{EVENT_SERVICE_URL}/api/events/{event_id}")
    return handle_response(response)

# Group Service Endpoints
@app.post("/groups/create")
async def create_group(group_data: GroupModel):
    response = requests.post(f"{GROUP_SERVICE_URL}/groups/create", json=group_data.model_dump())
    return handle_response(response)

@app.get("/groups/{group_id}")
async def get_group(group_id: str):
    response = requests.get(f"{GROUP_SERVICE_URL}/groups/{group_id}")
    return handle_response(response)

@app.put("/groups/update/{group_id}")
async def update_group(group_id: str, group_data: dict = Body(...)):
    response = requests.put(f"{GROUP_SERVICE_URL}/groups/update/{group_id}", json=group_data)
    return handle_response(response)

@app.delete("/groups/delete/{group_id}")
async def delete_group(group_id: str):
    response = requests.delete(f"{GROUP_SERVICE_URL}/groups/delete/{group_id}")
    return handle_response(response)

def handle_response(response):
    try:
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


# Synchronous call demonstration
@app.get("/sync-demo")
def synchronous_demo():
    event_status = requests.get(f"{EVENT_SERVICE_URL}").json()
    print("Event Service Response:", event_status)
    
    group_status = requests.get(f"{GROUP_SERVICE_URL}").json()
    print("Group Service Response:", group_status)
    
    user_status = requests.get(f"{USER_SERVICE_URL}").json()
    print("User Service Response:", user_status)

    return {"event_service": event_status, "group_service": group_status, "user_service": user_status}


# Asynchronous call demonstration
@app.get("/async-demo")
async def asynchronous_demo():
    services = [GROUP_SERVICE_URL, USER_SERVICE_URL, EVENT_SERVICE_URL]
    service_names = ["Group Service", "User Service", "Event Service"]
    responses = []
    
    coroutines = [check_service_status(service, name) for service, name in zip(services, service_names)]
    tasks = [asyncio.create_task(coro) for coro in coroutines]
    # tasks = [asyncio.create_task(check_service_status(services[i], service_names[i])) for i in range(len(services))]
    for task in asyncio.as_completed(tasks):
        response = await task
        responses.append(response)
  
    return {"status": "Completed asynchronous checks", "responses": responses}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
