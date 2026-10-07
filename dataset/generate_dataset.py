"""
Generate a realistic facility inspection dataset for Day 3.

The generated raw dataset intentionally contains:
- 5 duplicate rows
- missing values in cleanliness_score, odor_score and water_availability
- 3 invalid negative complaint values
- 4 extreme footfall outliers

Usage:
    python dataset/generate_dataset.py
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
ROW_COUNT = 150
FACILITY_START_ID = 101

LOCATIONS = [
    "North Wing",
    "South Wing",
    "East Concourse",
    "West Terminal",
    "Central Hub",
]

WASTE_LEVELS = ["Low", "Medium", "High", "Critical"]


def generate_dataset() -> pd.DataFrame:
    """Generate clean-looking base records, then inject controlled dirty data."""
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    today = date.today()
    start_date = today - timedelta(days=89)

    location_effects = {
        "North Wing": 0.30,
        "South Wing": -0.20,
        "East Concourse": 0.10,
        "West Terminal": -0.40,
        "Central Hub": 0.50,
    }

    records = []

    for i in range(ROW_COUNT):
        location = random.choice(LOCATIONS)

        cleanliness = np.clip(
            rng.normal(7.0 + location_effects[location], 1.05),
            1.0,
            10.0,
        )

        odor = np.clip(
            3.1 - 0.22 * (cleanliness - 5.0) + rng.normal(0, 0.45),
            1.0,
            5.0,
        )

        waste_probabilities = {
            "Low": 0.38,
            "Medium": 0.37,
            "High": 0.18,
            "Critical": 0.07,
        }
        waste_level = random.choices(
            WASTE_LEVELS,
            weights=list(waste_probabilities.values()),
            k=1,
        )[0]

        water_available = "Yes" if random.random() < 0.82 else "No"

        base_footfall = {
            "North Wing": 1250,
            "South Wing": 1050,
            "East Concourse": 1700,
            "West Terminal": 1950,
            "Central Hub": 2200,
        }[location]

        footfall = int(np.clip(rng.normal(base_footfall, 350), 200, 2500))

        complaint_lambda = (
            2.5
            + max(0, 3.2 - cleanliness) * 1.7
            + max(0, odor - 2.0) * 2.0
            + (2.0 if water_available == "No" else 0.0)
            + (1.5 if waste_level in {"High", "Critical"} else 0.0)
        )
        complaints = int(np.clip(rng.poisson(max(0.5, complaint_lambda)), 0, 30))

        inspection_date = start_date + timedelta(
            days=random.randint(0, 89)
        )

        records.append(
            {
                "facility_id": f"FAC_{FACILITY_START_ID + i}",
                "location": location,
                "cleanliness_score": round(float(cleanliness), 2),
                "odor_score": round(float(odor), 2),
                "waste_level": waste_level,
                "water_availability": water_available,
                "footfall": footfall,
                "complaints": complaints,
                "inspection_date": inspection_date.isoformat(),
            }
        )

    df = pd.DataFrame(records)

    # 8% missing values in each requested column.
    missing_count = max(1, round(ROW_COUNT * 0.08))
    for column in [
        "cleanliness_score",
        "odor_score",
        "water_availability",
    ]:
        indices = rng.choice(df.index, size=missing_count, replace=False)
        df.loc[indices, column] = np.nan

    # Three intentionally invalid negative complaint values.
    invalid_indices = rng.choice(df.index, size=3, replace=False)
    df.loc[invalid_indices, "complaints"] = [-5, -2, -8]

    # Four extreme footfall outliers.
    outlier_indices = rng.choice(df.index, size=4, replace=False)
    outlier_values = [18000, 22000, 25000, -500]
    for idx, value in zip(outlier_indices, outlier_values):
        df.loc[idx, "footfall"] = value

    # Exactly five duplicate records.
    duplicate_indices = rng.choice(df.index, size=5, replace=False)
    duplicates = df.loc[duplicate_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    return df


def main() -> None:
    output_path = Path(__file__).resolve().parent / "raw_facility_data.csv"
    df = generate_dataset()
    df.to_csv(output_path, index=False)

    print("=" * 65)
    print("FACILITY DATASET GENERATION COMPLETE")
    print("=" * 65)
    print(f"Output: {output_path}")
    print(f"Rows generated: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\nRaw dataset intentionally contains:")
    print("- 5 duplicate rows")
    print("- 8% missing values in selected fields")
    print("- 3 negative complaint values")
    print("- 4 extreme footfall outliers")


if __name__ == "__main__":
    main()
