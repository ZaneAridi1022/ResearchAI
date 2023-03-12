import time
import asyncio
from recommend import Recommendation

# create an instance of the Recommendation class
# call the recommend function and measure the time taken
start_time = time.time()
topic = "climate change"
result = asyncio.run(Recommendation().recommend(topic))
end_time = time.time()
time_taken = end_time - start_time

# print the result and the time taken
print("Result:", result)
print("Time taken:", time_taken, "seconds")