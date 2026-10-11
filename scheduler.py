##converts the time in hours and mins to just mins to compare to each other
def timeToMinutes(time_str):
    hours, minutes = time_str.strip().split(":")
    return int(hours) *60 + int(minutes)
##converts chunks like MWF into {M,W,F} also changes Th to R for simplicity of single letters
def parse_days(days_str):
    days_str = days_str.strip().replace("Th", "R")
    return list(days_str)
##turns the lines in the index into dictionaries
def parse_line(line):
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise ValueError(f"Expected 5 fields but got {len(parts)}: {line}")
    course, section, days, start, end = parts
    return{ "course":course,
    "section": section,
    "days": parse_days(days),
    "start": timeToMinutes(start),
    "end":timeToMinutes(end),}
##parses the whole index.html textbox and seperates it into a line for each class
def parse_courses(text):
    courses = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        section = parse_line(line)
        name = section["course"]
        if name not in courses:
            courses[name] = []
        courses[name].append(section)
    return courses
##checks the dates and start and end times of classes and determines if there are any conflicts
def conflict_Checker(a,b):
    shared_days = set(a["days"]) & set(b["days"])
    if not shared_days:
        return False
    return a["start"]<b["end"] and b["start"] < a["end"]
##checks to see if a combination of classes is valid for the schedule
def is_valid(schedule):
    return not any(conflict_Checker(a,b) for a, b in itertools.combinations(schedule,2))
##Checks if any classes start before 10 and assigns them negative points if they do
def early_penalty(schedule):
    return sum(10 for s in schedule if s["start"] < 600)
##Checks if any classes are on friday and assigns negative points if they are
def friday_penalty(schedule):
    return 25 if any("F" in s["days"] for s in schedule) else 0
##determines the gap between classes and ranks them based on minimizing the gap
def gap_penalty(schedule):
    total_gap = 0
    for day in ["M","T","W","R","F"]:
        classes = sorted((s for s in schedule if day in s["days"]), key = lambda s: s["start"])
        for earlier, later in zip(classes, classes[1:]):
            total_gap += later["start"] - earlier["end"]
        return total_gap // 10
##totals up the score of each class
def score(schedule, no_early, fridays_free, min_gaps):
    points = 100
    if no_early:
        points -=early_penalty(schedule)
    if fridays_free:
        points -= friday_penalty(schedule)
    if min_gaps:
        points -= gap_penalty(schedule)
    return points
##determines the best possible schedule based off scores
def best_schedules(courses, no_early, fridays_free, min_gaps, top_n=3):
    all_combos = itertools.product(*courses.values())
    valid = [list(c) for c in all_combos if is_valid(c)]
    valid.sort(key= lambda s: score(s,no_early, fridays_free, min_gaps), reverse = True)
    return valid[:top_n]