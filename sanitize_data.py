from pathlib import Path
import json

JSON_PATH = Path.cwd() / "student_data.json"
CLEANED_PATH = Path.cwd() / "cleaned_data.json"

with open(JSON_PATH) as f:
    data = json.load(f)

cleaned_data = []

for i, student in enumerate(data[2:], 1):
    student["name"] = f"student{i}"
    student["email"] = f"student{i}@pybites.org"
    student["profile_url"] = f"https://codechalleng.es/profiles/student{i}"
    student["certificates"] = ""
    cleaned_data.append(student)


with open(CLEANED_PATH, "w") as f:
    json.dump(cleaned_data, f)
