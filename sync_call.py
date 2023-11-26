import requests

def call_user_service():
	response = requests.get("http://user-service/api")
	print("User Service Response:", response.json())

def call_event_service():
	response = requests.get("http://18.224.62.48:8011/")
	print("Event Service Response:", response.json())

def call_group_service():
	response = requests.get("http://group-service/api")
	print("Group Service Response:", response.json())

def main():
	
	try:
		call_user_service()
	except:
		pass
	
	try:
		call_event_service()
	except:
		pass

	try:	
		call_group_service()
	except:
		pass

if __name__ == "__main__":
	main()
