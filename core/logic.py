# =========================
# CORE CALCULATIONS
# =========================

def calculate_health(initial, current):
    if initial == 0:
        return 0
    return max(0, min((current / initial) * 100, 100))


def calculate_wear_rate(initial, current, distance):
    if distance == 0:
        return 0
    # FIX: No negative wear
    return max(0, (initial - current) / distance)


def calculate_rul(current, wear_rate):
    if wear_rate == 0:
        return 9999
    return max(0, current / wear_rate)


# =========================
# ANALYSIS
# =========================

def behavior_factor_v2(braking, distance):
    if distance == 0:
        return 1

    ratio = braking / distance

    if ratio > 0.3:
        return 0.9
    elif ratio > 0.1:
        return 0.95
    return 1


def smart_health_v2(health, factor, wear):
    if wear < 0.001:
        return health
    adjusted = health - (1 - factor) * 5
    return max(0, min(adjusted, 100))


def classify_risk(health, rul):
    if health < 10:
        return "CRITICAL"
    elif health < 20:
        return "HIGH"
    elif health < 50:
        return "MODERATE"
    return "NORMAL"


def detect_driving_style(braking, distance):
    if distance == 0:
        return "Unknown"

    rate = braking / distance

    if rate > 0.8:
        return "Aggressive"
    elif rate > 0.5:
        return "Moderate"
    return "Smooth"


def detect_trend(wear):
    return "Rapid Wear" if wear > 0.002 else "Normal Wear"


def brake_usage(braking, distance):
    ratio = braking / max(distance, 1)

    if ratio > 0.8:
        return "High Brake Stress"
    elif ratio > 0.5:
        return "Moderate Usage"
    return "Smooth Usage"


def usage_pattern(braking, distance):
    ratio = braking / max(distance, 1)
    return "City Driving" if ratio > 0.04 else "Highway Driving"


def environment_factor(location):
    loc = location.lower()

    if loc in ["mumbai", "chennai"]:
        return "High Humidity"
    elif loc in ["pune", "bangalore"]:
        return "Moderate Conditions"
    return "Normal Conditions"


def failure_probability(health):
    if health < 10:
        return "Very High"
    elif health < 20:
        return "High"
    elif health < 40:
        return "Medium"
    return "Low"


# =========================
# AI CONFIDENCE
# =========================

def ai_confidence_v2(health, wear, braking, distance):

    ratio = braking / distance if distance != 0 else 0

    if health < 20:
        health_strength = 1.0
    elif health < 50:
        health_strength = 0.7
    else:
        health_strength = 0.5

    if wear > 0.003:
        wear_strength = 1.0
    elif wear > 0.001:
        wear_strength = 0.7
    else:
        wear_strength = 0.5

    if wear < 0.001 and ratio > 0.2:
        agreement = 0.6
    elif wear > 0.002 and ratio > 0.2:
        agreement = 1.0
    else:
        agreement = 0.8

    if (health < 30 and wear > 0.002) or (health > 60 and wear < 0.001):
        certainty = 1.0
    else:
        certainty = 0.75

    confidence = (
        0.4 * health_strength +
        0.3 * wear_strength +
        0.2 * agreement +
        0.1 * certainty
    ) * 100

    return round(confidence, 2)