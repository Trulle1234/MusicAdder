# pip install pycountry requests
import os
import requests
import pycountry

# ◉ Base-names (from asia_anthems/*.mid, no “.png”)
names = [
    "afghanistan","bahrain","bangladesh","bhutan","brunei","cambodia","china",
    "india","indonesia","iran","iraq","israel","japan","jordan","kazakhstan",
    "kuwait","kyrgyzstan","laos","lebanon","malaysia","maldives","mongolia",
    "myanmar","nepal","north_korea","oman","pakistan","philippines","qatar",
    "saudiarabia","singapore","south_korea","sri_lanka","syria","tajikistan",
    "thailand","timorleste","turkmenistan","uae","uzbekistan","vietnam","yemen"
]

# ◉ Fallbacks for lookups that don’t map cleanly
override = {
    "north_korea":    "kp",
    "south_korea":    "kr",
    "saudiarabia":    "sa",
    "timorleste":     "tl",  # East Timor
    "uae":            "ae",
     "brunei":         "bn",
    #…add more if you see any “Could not find” warnings
}

# ◉ Where to save
output_dir = os.path.abspath("flags")
os.makedirs(output_dir, exist_ok=True)
print("Saving flags into:", output_dir)

for name in names:
    key = name.replace("_", " ").title()  # e.g. "north_korea"→"North Korea"
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