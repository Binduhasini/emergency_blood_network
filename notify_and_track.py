from datetime import datetime

def notify_donors(ranked_donors, message):
    for donor in ranked_donors:
        print(f"Notifying {donor['name']} at {donor['email']} / {donor['contact_number']} "
              f"({donor.get('distance_km', '?')} km away): {message}")
    return ranked_donors


def update_response(donor_id, response, donors):
    for donor in donors:
        if donor["donor_id"] == donor_id:
            donor.setdefault("response_history", []).append({
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            print(f"Logged response for {donor['name']}: {response}")
            return
    print(f"No donor found with ID {donor_id}")


if __name__ == "__main__":
    from filter_donor import load_donors, filter_donors
    from distance_calc import rank_by_distance

    donors = load_donors("donors.csv")
    eligible = filter_donors(donors, "O-")
    ranked = rank_by_distance(eligible, -33.8688, 151.2093)

    notified = notify_donors(ranked, "Urgent: O- blood needed at City Hospital")

    if notified:
        update_response(notified[0]["donor_id"], "yes", notified)