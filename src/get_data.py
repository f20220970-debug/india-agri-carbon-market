"""Fetch the emissions dataset.  python src/get_data.py  (~15 MB)

Our World in Data's CO2 and greenhouse gas dataset: country-year emissions
including methane, built from the Global Carbon Project and Climate Watch.
Used here only for India's national methane level and trend; the market model
is built on rice area, not on this.
"""
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
OUT = Path(__file__).resolve().parents[1] / "data" / "owid.csv"

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        print(f"already present: {OUT}")
    else:
        print("downloading ~15 MB")
        urllib.request.urlretrieve(URL, OUT)
        print("saved", OUT)
