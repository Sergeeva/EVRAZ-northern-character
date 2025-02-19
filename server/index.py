from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformData import transformData
from getRawData import getRawData
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def findExhausterById(exhausters, id):
    # TODO
    for ex in exhausters:
        if ex.id == id:
            return ex

    return {'error': 'exhauster not found'}


@app.get('/api/get-all-exhausters')
async def getAllExhausters():
    '''Get sensor data from Kafka and transform it into array of exhausters'''
    rawData = getRawData()
    response = transformData(rawData)

    return response

@app.get('/api/get-all-exhausters-cache-test')
async def getAllExhausters():
    '''Get pre-loaded test data and transform it into array of exhausters'''
    with open('message-cache.json', encoding='utf-8') as f:
        rawData = json.load(f)
    response = transformData(rawData)

    return (response)


@app.get('/api/get-exhauster/{id}')
async def getAllExhausters(id):
    rawData = getDataFromKafka()
    allExhausters = transformData(rawData)
    # find exhauster with the given id
    response = findExhausterById(allExhausters, id)

    return response
