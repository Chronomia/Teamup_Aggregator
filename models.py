from pydantic import BaseModel
from typing import List, Optional

class GroupModel(BaseModel):
    group_id: str
    group_name: str
    founder: str
    city: str
    state: str
    category: str
    intro: str
    policy: str

class Event(BaseModel):
	event_id: str
	status: str
	capacity: int
	event_name: str
	description: str
	location: str
	time: str
	group_id: str
	organizer_id: str
	tag_1: str
	tag_2: Optional[str]
	duration: int