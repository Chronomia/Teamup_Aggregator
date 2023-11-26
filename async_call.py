import asyncio
import aiohttp
import random

# Define a list of microservices with their URLs and types
microservices = [
	{"url": "http://18.224.62.48:8011/api/events/1/comments", "type": "User Service"},
	{"url": "http://18.224.62.48:8011/", "type": "Event Service"},
	{"url": "http://18.224.62.48:8011/api/events", "type": "Group Service"}
]

async def call_microservice(session, microservice):
	url, service_type = microservice["url"], microservice["type"]
	async with session.get(url) as response:
		result = await response.text()
		print(f"Response from {service_type} : {result}")

async def main():
	for _ in range(10):
		print("======= Iteration {} =======".format(_ + 1))
		print("")
		async with aiohttp.ClientSession() as session:
			tasks = [call_microservice(session, service) for service in microservices]
			random.shuffle(tasks)  # Shuffle to ensure different order
			await asyncio.gather(*tasks)
		print("")

asyncio.run(main())

