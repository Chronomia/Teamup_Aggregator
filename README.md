# Teamup_Aggregator

## Overview
A FastAPI application to aggregate and interact with various microservices. It includes health check endpoints, event and group management, and demonstrations of synchronous and asynchronous calls.


## Endpoints

### Health Checks
- `GET /check/event-service`: Check the status of the Event Service.
- `GET /check/group-service`: Check the status of the Group Service.
- `GET /check/user-service`: Check the status of the User Service.

### Event Service
- `POST /events/create`: Create an event.
- `GET /events/{event_id}`: Get event details.
- `PUT /events/{event_id}/update_name`: Update event name.
- `DELETE /events/{event_id}`: Delete an event.

### Group Service
- `POST /groups/create`: Create a group.
- `GET /groups/{group_id}`: Get group details.
- `PUT /groups/update/{group_id}`: Update group.
- `DELETE /groups/delete/{group_id}`: Delete a group.

### Demonstrations
- `GET /sync-demo`: Demonstrates synchronous calls to microservices.
- `GET /async-demo`: Demonstrates asynchronous calls to microservices.
