from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

    return f"""
    <h2>Recieved:</h2>
    <pre>{courses}</pre>
    <p>No Early: {no_early} | Fridays free: {fridays_free} | Min gaps: {min_gaps}</p>
    <a href="/">Back</a>
    """