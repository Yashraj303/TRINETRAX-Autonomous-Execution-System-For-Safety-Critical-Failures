import os 
import requests
from core.logic import *

# =========================
# SERVICE STATUS FILE
# =========================
STATUS_FILE = "service_status.txt"

API_KEY = "YOUR_API_KEY_HERE"

# =========================
# ENSURE FILE EXISTS
# =========================
if not os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "w") as f:
        f.write("not_booked")


# =========================
# SERVICE CENTER FETCH (API ONLY)
# =========================
def get_service_centers():
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": "18.5204,73.8567",
        "radius": 5000,
        "type": "car_repair",
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=3)
    data = response.json()

    centers = []

    if data.get("status") == "OK":
        for place in data["results"][:3]:
            name = place.get("name", "Service Center")

            maps_link = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}"

            centers.append({
                "name": name,
                "distance": "Nearby",
                "maps_link": maps_link
            })

    return centers


# =========================
# SERVICE BOOKING CONTROL
# =========================
def is_service_booked():
    try:
        with open(STATUS_FILE, "r") as f:
            return f.read().strip() == "booked"
    except:
        return False


def set_service_booked():
    with open(STATUS_FILE, "w") as f:
        f.write("booked")


def reset_service_status():
    with open(STATUS_FILE, "w") as f:
        f.write("not_booked")


# =========================
# DATA AGENT 
# =========================
def data_agent(initial, current, distance, braking):
    return {
        "initial": float(initial),
        "current": float(current),
        "distance": float(distance),
        "braking_events": int(braking)
    }


# =========================
# DIAGNOSIS AGENT
# =========================
def diagnosis_agent(data):

    health = calculate_health(data["initial"], data["current"])
    wear = calculate_wear_rate(data["initial"], data["current"], data["distance"])
    rul = calculate_rul(data["current"], wear)

    factor = behavior_factor_v2(data["braking_events"], data["distance"])
    smart = smart_health_v2(health, factor, wear)

    style = detect_driving_style(data["braking_events"], data["distance"])
    trend = detect_trend(wear)

    usage = brake_usage(data["braking_events"], data["distance"])
    env = environment_factor("pune")
    pattern = usage_pattern(data["braking_events"], data["distance"])

    failure = failure_probability(smart)

    confidence = ai_confidence_v2(
        smart,
        wear,
        data["braking_events"],
        data["distance"]
    )

    # DEBUG (VERY IMPORTANT)
    print("DEBUG → Health:", smart, "| Wear:", wear, "| RUL:", rul)

    return smart, wear, rul, style, trend, usage, env, pattern, failure, confidence


# =========================
# DECISION AGENT (UNCHANGED + DEBUG)
# =========================
def decision_agent(health, rul):
    risk = classify_risk(health, rul)

    # DEBUG
    print("DEBUG → Risk:", risk)

    return risk