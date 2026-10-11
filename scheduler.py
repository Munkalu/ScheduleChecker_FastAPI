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
