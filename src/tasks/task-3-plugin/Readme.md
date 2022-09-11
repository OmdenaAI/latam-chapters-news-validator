# Chrome extension code

## Index

1. [Backend](#backend)
2. [Frontend](#frontend)
3. [Setup](#setup)

## Backend

`backend` folder contains the code of a FastAPI RESTful API. The main endpoint `upload` saves the webpage information reported by the user using the Chrome plugin.

The API is deployed in a [micro](https://docs.deta.sh/docs/micros/about) Deta instance: 

## Frontend

`frontend` folder contains the code executed by Chrome to show the plugin.

## Setup

1. Enable 'Developer mode' in chrome extension settings.
2. Load frontend folder with 'Load unpacked' button in chrome.
