# Emergency Blood Donor System

When a hospital urgently needs blood, this little tool helps track down the right donors fast. Give it a blood group and a city, and it'll pull up nearby eligible donors, sorted by distance, so you can start reaching out to the closest one first.

It started as a group project, so you'll see the workflow split across a few files rather than one big script — each one handles a specific part of the process (filtering, distance, notifying).

## What it actually does

- **Finds who's eligible** — checks blood group, availability, and makes sure they haven't donated too recently (`filter_donor.py`)
- **Figures out who's closest** — calculates real distance to the hospital using the Haversine formula, so you're not guessing (`distance_calc.py`)
- **Reaches out and keeps notes** — notifies donors and logs whether they said yes, no, or didn't respond, with a timestamp (`notify_and_track.py`)
- **Ties it all together** — one script that walks you through the whole thing end to end (`main.py`)

## Project Structure

```
.
├── main.py               # CLI entry point — orchestrates the full workflow
├── filter_donor.py       # Loads donors.csv and filters eligible donors
├── distance_calc.py      # Haversine distance calculation + ranking
├── notify_and_track.py   # Donor notification + response logging
└── donors.csv            # Donor dataset (not included — see below)
```

## Requirements

- Python 3.8+
- No external dependencies (uses only the standard library: `csv`, `math`, `json`, `datetime`)

## Getting Started

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```
2. Drop a `donors.csv` file into the project root. It needs these columns:
   ```
   donor_id, name, email, contact_number, city, blood_group,
   availability, months_since_first_donation, number_of_donation,
   pints_donated, created_at, lat, long
   ```

## How to Use It

Just run:

```bash
python main.py
```

It'll ask you two things:
1. **What blood group do you need?** (e.g. `O+`, `A-`, `AB+`)
2. **Which hospital city?** (Sydney, Melbourne, Brisbane, Perth, Adelaide, Canberra, Hobart, Darwin)

From there it takes care of the rest:
1. Filters donors who match the blood group and are actually available
2. Sorts them by how close they are to the hospital
3. Notifies everyone on that list
4. Asks you to log each donor's response as you get it (`yes` / `no` / `no response`)
5. Stops as soon as someone confirms — otherwise it moves on to the next closest donor
6. Saves everything (including the full response history) to `donors_updated.json` when it's done

### Testing individual pieces

You don't have to run the whole flow to check a single module — each one works on its own:

```bash
python filter_donor.py      # See eligible donors for every blood group at once
python distance_calc.py     # See eligible donors ranked by distance
```

## What counts as "eligible"

A donor makes the cut if:
- Their blood group matches what's needed (not case-sensitive, so `o+` and `O+` are treated the same)
- They've marked themselves as available
- Enough time has passed since their last donation — we estimate this by dividing months since their first donation by how many times they've donated, and it needs to be at least 3 months (stored as `estimated_avg_gap_months`)

## A few things to double check

- `notify_and_track.py` assumes every donor has an `email` field — worth double-checking your CSV has that column filled in.
- If you run `distance_calc.py` on its own, heads up that it looks for `donor.csv` (no "s"), not `donors.csv`. Easy to miss.

## License

Add your license here.