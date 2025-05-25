# pip install pycountry requests
import os
import requests
import pycountry

# List exactly as your MIDI base-names (no “.mid”)
names = [
    "albania","andorra","armenia","austria","azerbaijan","belarus","belgium",
    "bosnia","bulgaria","croatia","czechia","denmark","finland","france",
    "georgia","germany","gibraltar","greece","guernsey","hungary","iceland",
    "ireland","Isle_of_man","italy","jersey","latvia","lithuania","luxembourg",
    "macedonia","malta","moldova","monaco","montenegro","netherlands","norway",
    "poland","portugal","romania","russia","san_marino","serbia","slovakia",
    "slovenia","spain","sweden","switzerland","turkey","uk","ukraine","vatican"
]

# Special cases where pycountry lookup or flagcdn code differs
override = {
    "czechia":    "cz",  # Czech Republic
    "macedonia":  "mk",  # North Macedonia
    "bosnia":     "ba",  # Bosnia & Herzegovina
    "san_marino": "sm",
    "isle_of_man":"im",
    "guernsey":   "gg",
    "jersey":     "je",
    "gibraltar":  "gi",
    "vatican":    "va",
    "uk":         "gb",  # United Kingdom
    "russia":      "ru",
    "turkey":      "tr",
}

output_dir = os.path.join(os.path.dirname(__file__), "flags")
os.makedirs(output_dir, exist_ok=True)

for name in names:
    key = name.replace("_", " ").title()  # e.g. "Isle_of_man"→"Isle Of Man"
    try:
        country = pycountry.countries.lookup(key)
        code = country.alpha_2.lower()
    except LookupError:
        code = override.get(name.lower())
        if not code:
            print(f"⚠️ Could not find ISO code for “{name}” – skipping")
            continue

    url = f"https://flagcdn.com/w320/{code}.png"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        path = os.path.join(output_dir, f"{name}.png")
        with open(path, "wb") as f:
            f.write(resp.content)
        print(f"✅ Saved {name}.png")
    else:
        print(f"❌ Failed to download flag for {name} (HTTP {resp.status_code})")
