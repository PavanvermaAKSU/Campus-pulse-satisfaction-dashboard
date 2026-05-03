import pandas as pd
import random
from datetime import datetime, timedelta

num_rows = 500

academic_years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
majors = ["CSE", "AIDS", "ECE", "ME", "CE", "BBA"]
facilities = ["Library", "Canteen", "Hostel", "Transport", "Lab", "Classroom", "Sports"]

positive_comments = {
    "Library": [
        "Library is clean and useful",
        "Very satisfied with library environment",
        "Library has good study space",
        "Books are easily available",
        "Library services are excellent"
    ],
    "Canteen": [
        "Food quality is good",
        "Canteen is clean and spacious",
        "Service is fast and helpful",
        "Snacks are fresh and tasty",
        "Canteen experience is nice"
    ],
    "Hostel": [
        "Hostel rooms are comfortable",
        "Hostel maintenance is good",
        "Hostel environment is peaceful",
        "Rooms are clean and safe",
        "Satisfied with hostel services"
    ],
    "Transport": [
        "Transport service is excellent",
        "Buses are mostly on time",
        "Transport is convenient",
        "Bus staff is cooperative",
        "Very satisfied with transport"
    ],
    "Lab": [
        "Lab equipment is good",
        "Lab sessions are very helpful",
        "Lab environment is excellent",
        "Systems work properly",
        "Practical learning is effective"
    ],
    "Classroom": [
        "Classrooms are clean and comfortable",
        "Teaching environment is good",
        "Projector and seating are fine",
        "Classroom atmosphere is positive",
        "Satisfied with classroom facilities"
    ],
    "Sports": [
        "Sports facilities are good",
        "Ground is well maintained",
        "Coaching support is helpful",
        "Sports environment is motivating",
        "Equipment is available and useful"
    ]
}

negative_comments = {
    "Library": [
        "Library needs more books",
        "Library seating is limited",
        "Library is sometimes noisy",
        "Need improvement in library timing",
        "Issue with book availability"
    ],
    "Canteen": [
        "Canteen food quality is poor",
        "Service is slow",
        "Canteen is crowded",
        "Food is expensive",
        "Need improvement in hygiene"
    ],
    "Hostel": [
        "Hostel rooms need improvement",
        "Maintenance is poor",
        "Water supply has issues",
        "Rooms are crowded",
        "Hostel cleanliness is average"
    ],
    "Transport": [
        "Buses are often late",
        "Transport timing is not reliable",
        "Need more buses",
        "Transport service is average",
        "Delay causes problems"
    ],
    "Lab": [
        "Lab equipment needs upgrade",
        "Some systems do not work",
        "Lab is overcrowded",
        "Internet is slow in lab",
        "Need improvement in practical support"
    ],
    "Classroom": [
        "Classroom seating is uncomfortable",
        "Projector issues happen often",
        "Classroom maintenance is poor",
        "Rooms need better ventilation",
        "Classroom cleanliness is average"
    ],
    "Sports": [
        "Sports equipment is limited",
        "Ground maintenance is poor",
        "Need more sports support",
        "Facilities need improvement",
        "Practice timing is not managed well"
    ]
}

neutral_comments = {
    "Library": [
        "Library is average",
        "Library is okay overall",
        "Decent experience in library"
    ],
    "Canteen": [
        "Canteen is okay",
        "Food is average",
        "Average experience in canteen"
    ],
    "Hostel": [
        "Hostel is average",
        "Hostel experience is okay",
        "Facilities are manageable"
    ],
    "Transport": [
        "Transport is average",
        "Bus service is okay",
        "Average transport experience"
    ],
    "Lab": [
        "Lab is okay",
        "Average lab experience",
        "Lab support is manageable"
    ],
    "Classroom": [
        "Classroom is okay",
        "Average classroom experience",
        "Facilities are manageable"
    ],
    "Sports": [
        "Sports facilities are average",
        "Okay sports experience",
        "Facilities are manageable"
    ]
}


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


data = []

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 4, 1)

for i in range(1, num_rows + 1):
    student_id = 1000 + i
    academic_year = random.choice(academic_years)
    major = random.choice(majors)
    facility = random.choice(facilities)

    score = random.randint(1, 5)

    if score >= 4:
        comment = random.choice(positive_comments[facility])
    elif score == 3:
        comment = random.choice(neutral_comments[facility])
    else:
        comment = random.choice(negative_comments[facility])

    timestamp = random_date(start_date, end_date).strftime("%Y-%m-%d")

    data.append({
        "student_id": student_id,
        "academic_year": academic_year,
        "major": major,
        "facility_rated": facility,
        "satisfaction_score": score,
        "timestamp": timestamp,
        "comment": comment
    })

df = pd.DataFrame(data)

df.to_csv("data/student_satisfaction.csv", index=False)

print("Dataset generated successfully with", len(df), "rows")
print(df.head())