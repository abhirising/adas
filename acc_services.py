# ----------------------------
# ACC SERVICE
# ----------------------------

def decide_acc(distance, rel_speed, ego_speed, cfg):

    safe_distance = cfg["safe_distance"]
    max_accel = cfg["max_accel"]
    max_decel = cfg["max_decel"]
    inc = cfg["speed_increment"]
    dec = cfg["speed_decrement"]

    if distance < safe_distance:
        target_speed = max(0, ego_speed - dec)
        accel = max_decel
        status = "FOLLOW / SLOW DOWN"

    else:
        target_speed = ego_speed + inc
        accel = max_accel
        status = "CRUISE"

    return {
        "target_speed": target_speed,
        "acceleration": accel,
        "status": status
    }