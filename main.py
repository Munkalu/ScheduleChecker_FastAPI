from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scheduler import parse_courses

app = FastAPI()
templates = Jinja2Templates(directory ="templates")


@app.get("/", response_class = HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/schedule", response_class= HTMLResponse)
def schedule(
    courses: str = Form(...),
    no_early: bool = Form(False),
    fridays_free: bool = Form(False),
    min_gaps: bool = Form(False),
):

    parsed = parse_courses(courses)
    return f"<pre>{parsed}</pre><a href = '/'>Back</a>"