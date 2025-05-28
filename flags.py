# pip install pycountry requests
import os
import requests
import pycountry

# ◉ Base-names (no “.png”)
names = [
    "american_samoa","australia","cook_islands","fiji","guam","kiribati",
    "marshall_islands","micronesia","nauru","new_zealand","niue",
    "northern_marianas","palau","papua_new_guinea","pitcairn","samoa",
    "solomon_islands","tokelau","tonga","tuvalu","vanuatu"
]

# ◉ Fallbacks where lookup may fail or hyphens/spaces differ
override = {
    "american_samoa":     "as",
    "cook_islands":       "ck",
    "marshall_islands":   "mh",
    "micronesia":         "fm",
    "new_zealand":        "nz",
    "northern_marianas":  "mp",
    "papua_new_guinea":   "pg",
    "pitcairn":           "pn",
    "solomon_islands":    "sb",
    "tokelau":            "tk",
    # most others map cleanly:
    # "australia": "au"
    # "fiji":       "fj"
    # "guam":       "gu"
    # "kiribati":   "ki"
    # "nauru":      "nr"
    # "niue":       "nu"
    # "palau":      "pw"
    # "samoa":      "ws"
    # "tonga":      "to"
    # "tuvalu":     "tv"
    # "vanuatu":    "vu"
}

output_dir = os.path.abspath("oceania_flags")
os.makedirs(output_dir, exist_ok=True)
print("Saving flags into:", output_dir)

for name in names:
    key = name.replace("_", " ").title()
    try:
        country = pycountry.countries.lookup(key)
        code = country.alpha_2.lower()
    except LookupError:
        code = override.get(name)
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
