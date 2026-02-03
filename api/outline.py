from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def get_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    headers = {"User-Agent": "GlobalEduBot/1.0"}

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    outline = ["## Contents\n"]
    for h in headings:
        level = int(h.name[1])
        outline.append("#" * level + " " + h.get_text(strip=True))

    return "\n".join(outline)
