import asyncio
import time

from backend.advaitflask import Recommendation

prompt = "machine learning"
recommendation = Recommendation()

start_time = time.time()
urls = asyncio.run(recommendation.recommend(prompt))
end_time = time.time()

duration = end_time - start_time
print(f"Request took {duration:.2f} seconds.")

print(urls)
