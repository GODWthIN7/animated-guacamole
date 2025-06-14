"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = [
    {
        "id": 1,
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    {
        "id": 2,
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    {
        "id": 3,
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
]


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_id}/signup")
async def signup_for_activity(activity_id: int, signup: SignupRequest):
    activity = next((a for a in activities if a["id"] == activity_id), None)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    # Validate student is not already signed up
    if signup.email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    # Validate there's room in the activity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="No available spots in this activity")
    # Sign up the student
    activity["participants"].append(signup.email)
    return {"message": f"Signed up {signup.email} for {activity['name']}"}
    # Add more activities
    activities.extend([
        # Sports related
        {
            "id": 4,
            "name": "Soccer Team",
            "description": "Join the school soccer team and compete in local leagues",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": []
        },
        {
            "id": 5,
            "name": "Basketball Club",
            "description": "Practice basketball skills and play friendly matches",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        # Artistic
        {
            "id": 6,
            "name": "Drama Club",
            "description": "Act, direct, and participate in school theater productions",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": []
        },
        {
            "id": 7,
            "name": "Art Workshop",
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 16,
            "participants": []
        },
        # Intellectual
        {
            "id": 8,
            "name": "Mathletes",
            "description": "Solve challenging math problems and compete in math contests",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": []
        },
        {
            "id": 9,
            "name": "Science Club",
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": []
        }
    ])