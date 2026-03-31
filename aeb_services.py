# ----------------------------
# AEB SERVICE
# ----------------------------

def compute_ttc(dist, rel_speed):
    if rel_speed <= 0:
        return float("inf")
    return dist / rel_speed


def decide_aeb(dist, rel_speed):
    ttc = compute_ttc(dist, rel_speed)

    if ttc < 1.5:
        return {
            "brake": True,
            "level": "HARD",
            "ttc": ttc,
            "status": "AEB BRAKE",
            "color": (0, 0, 255)
        }

    elif ttc < 3.0:
        return {
            "brake": False,
            "level": "MEDIUM",
            "ttc": ttc,
            "status": "ACC SLOW DOWN",
            "color": (0, 165, 255)
        }

    else:
        return {
            "brake": False,
            "level": "NONE",
            "ttc": ttc,
            "status": "SAFE",
            "color": (0, 255, 0)
        }