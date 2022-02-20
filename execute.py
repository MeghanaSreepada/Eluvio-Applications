import asyncio
import aiohttp
import time
import base64
import random

# Creating cache in global scope so that concurrent batches can be executed without repeated calls for already cached data.
cache = {}

async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(id, session, batch_responses):
    global cache
    # Convert id to base64 to send in the Authorization header
    base64String = base64.b64encode(id.encode('ascii')).decode('ascii')
    headers = {
        "Authorization": base64String
    }
    # Perform the request
    async with session.get(f"https://challenges.qluv.io/items/{id}", headers=headers) as response:
        obj = await response.text()
        cache[id] = obj
        batch_responses[id] = obj


# Helper function that will process the batch before sending requests
async def process_batch(ids, conc_req):
    global cache
    batch_responses = {}
    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    session = aiohttp.ClientSession(connector=conn)
    ids_set = set(ids) # Remove duplicates
    to_be_processed = []
    already_cached = 0

    for i in ids_set:
        if i not in cache:
            to_be_processed.append(i)
        else:
            already_cached += 1
            batch_responses[i] = cache[i]

    # Create current threads to execute the requests
    now = time.time()
    await gather_with_concurrency(conc_req, *[get_async(i, session, batch_responses) for i in to_be_processed])
    time_taken = time.time() - now

    # Print the output and the time taken
    print("Time taken: ", time_taken)
    print("Already Cached:", already_cached)
    print("No. of unique responses: ", len(batch_responses))
    print()

    # Uncomment below line to see the responses
    # print("Responses:", batch_responses)
    
    await session.close()

async def main():
    batch_size = 300 # Increase/Decrease to see how the program performs
    max_id = 100
    ids = []
    for i in range(batch_size):
        ids.append(str(random.randint(1, max_id)))
    # print(ids)

    # Execute the first batch
    print('Processing batch 1. This might take a while depending on the batch size.')
    await process_batch(ids, 5)

    ids2 = []
    for i in range(batch_size):
        ids2.append(str(random.randint(1, max_id)))
    # Execute second batch and check if cached values are skipped
    print('Processing batch 2. This might take a while depending on the batch size.')
    await process_batch(ids2, 5)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Prevent Event loop closed error
asyncio.run(main())