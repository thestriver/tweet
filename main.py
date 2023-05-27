from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_oauthlib import OAuth1Session
import json
import os

from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/post_tweet/")
async def post_tweet(sender: str, value: int, receiver: str, transaction_hash: str):

    status = f"New TX Alert 🚨🚨! {sender} sent {value} LOOPS to {receiver}! in transaction {transaction_hash}"

    payload = {"text": status}

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

    json_response = response.json()

    return json_response
