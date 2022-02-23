# Eluvio Internship Assessment - Option 2 - Applications

This is my submission for Eluvio Internship Assessment.

### Prerequisites
- Python 3.x
- aiohttp
- asyncio (comes with python)
- base64 (comes with python)
- random (comes with python)
- time (comes with python)

### Instructions to execute
First install the prerequisites using pip package manager.

```
pip install aiohttp
```

Now we can execute the program by running the command below
```
python execute.py
```

### Parameters you can play with for random ids generation
Note: I have used numbers as IDs while generating the batches to test the program since it is easier to generate random numbers and does not need additional code for it. You can also pass non numeric IDs to the process_batch function and it should work without any issues.

All the parameters are present in the main function.
- batch_size - Used to generate batches of ids.
- max_id - Max possible id which can be generated. 

In case you would like to change the input IDs to something more realistic, you can pass them as a list to the preprocess_batch() function.