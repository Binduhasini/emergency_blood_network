import csv
def load_donors(csv_path):
    with open(csv_path,newline="")as file:
        reader=csv.DictReader(file)
        return list(reader)
def filter_donors(donors,required_blood_group,min_gap_months=3):
    required_blood_group=required_blood_group.strip().upper()
    eligible_donors=[]
    for donor in donors:
        blood_group = str(donor.get("blood_group", "")).strip().upper()
        availability = str(donor.get("availability", "")).strip().lower()
        if blood_group!=required_blood_group:
            continue
        if availability!="yes":
            continue
        try:
            first_donation = float(donor.get("months_since_first_donation", 0))
            total_donations = int(donor.get("number_of_donation", 0))
        except (TypeError, ValueError):
            continue

        if total_donations == 0:
            avg_gap = first_donation
        else:
            avg_gap = first_donation / total_donations

        if avg_gap < min_gap_months:
            continue
        
        donor["estimated_avg_gap_months"] = round(avg_gap, 1)
        eligible_donors.append(donor)
    return eligible_donors
def months_and_days(avg_gap):
    whole_months = int(avg_gap)
    remaining_fraction = avg_gap - whole_months
    days = round(remaining_fraction * 30)
    return whole_months, days
if __name__ == "__main__":
    dataset = load_donors("donors.csv")
 
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
 
    for blood_group in blood_groups:
        result = filter_donors(dataset, blood_group)
        print(f"\n{blood_group} - Found {len(result)} donor(s):")
        for donor in result:
            name = donor["name"]
            city = donor["city"]
            contact_number = donor["contact_number"]
            months, days = months_and_days(donor["estimated_avg_gap_months"])
            if days == 0:
                time_ago = f"{months} months"
            else:
                time_ago = f"{months} months {days} days"
            print(f"Name: {name} - City: {city} - Mobile Number: {contact_number} - Avg. Gap Between Donations: {time_ago} ago")
 