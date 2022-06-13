from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

#This should be a different database
redis = get_redis_connection(
    host="redis-12578.c276.us-east-1-2.ec2.cloud.redislabs.com",
    port="12578",
    password="yH8qVetKSdR8gySrZOse1U91DJ62NE7J",
    decode_responses=True
)
