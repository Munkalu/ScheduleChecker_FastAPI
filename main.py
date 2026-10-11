from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scheduler import parse_courses, best_schedules, score

app = FastAPI()
templates = Jinja2Templates(directory ="templates")
DAYS = [("M", "Monday"), ("T", "Tuesday"), ("W", "Wednesday"), ("R", "Thursday"), ("F", "Friday")]

##converts the pure minutes back into readable time
def minutes_to_time(m):
    hours, minutes = divmod(m, 60)
    suffix = "AM" if hours < 12 else "PM"
    return f"{hours % 12 or 12}:{minutes:02d} {suffix}"


templates.env.filters["time"] = minutes_to_time

@app.get("/", response_class = HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/schedule", response_class= HTMLResponse)
def schedule(
    request: Request,
    courses: str = Form(...),
    no_early: bool = Form(False),
    fridays_free: bool = Form(False),
    min_gaps: bool = Form(False),
):

    parsed = parse_courses(courses)
    top = best_schedules(parsed, no_early, fridays_free, min_gaps)

    results = []
    for sched in top:
        by_day = {
            code: sorted([s for s in sched if code in s["days"]], key=lambda s: s["start"])
            for code, _ in DAYS
        }
        results.append({
            "score": score(sched, no_early, fridays_free, min_gaps),
            "by_day": by_day,
        })

    return templates.TemplateResponse(
        request, "results.html", {"results": results, "days": DAYS, "error": None}
    )