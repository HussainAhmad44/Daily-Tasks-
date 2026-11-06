from fastapi import FastAPI

app = FastAPI()

hostels = [
    {"id": 1, "name": "City Hostel", "city": "Lahore", "rent": 12000},
    {"id": 2, "name": "Green Hostel", "city": "Lahore", "rent": 18000},
    {"id": 3, "name": "Blue Hostel", "city": "Islamabad", "rent": 15000}
]

@app.get("/hostels")
def get_hostels(
    city: str | None = None,
    max_rent: int | None = None
):
    result = hostels

    if city is not None:
        result = [
            h for h in result
            if h["city"].lower() == city.lower()
        ]

    if max_rent is not None:
        result = [
            h for h in result
            if h["rent"] <= max_rent
        ]

    return result


@app.get("/hostels/{hostel_id}")
def get_hostel(hostel_id: int):
    for hostel in hostels:
        if hostel["id"] == hostel_id:
            return hostel

    return {"error": "Hostel not found"}