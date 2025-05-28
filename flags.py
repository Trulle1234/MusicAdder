# pip install pycountry requests
import os
import requests
import pycountry

# ▶︎ Replace the European list with all African base-names (snake_case, no “.png”)
names = [
    "algeria","angola","benin","botswana","burkina_faso","burundi","cameroon",
    "cape_verde","central_african_republic","chad","comoros","congorep",
    "democratic_republic_of_the_congo","djibouti","egypt","equatorial_guinea",
    "eritrea","eswatini","ethiopia","gabon","gambia","ghana","guinea",
    "guinea_bissau","ivory_coast","kenya","lesotho","liberia","libya",
    "madagascar","malawi","mali","mauritania","mauritius","morocco",
    "mozambique","namibia","niger","nigeria","rwanda","sao_tome",
    "senegal","seychelles","sierra_leone","somalia","south_africa",
    "south_sudan","st_helena","sudan","tanzania","togo","tunisia",
    "uganda","zambia","zimbabwe"
]

# ▶︎ Only special cases where lookup fails:
override = {
    "cape_verde":                       "cv",
    "ivory_coast":                      "ci",
    "congorep":                         "cg",
    "democratic_republic_of_the_congo": "cd",
    "sao_tome":                         "st",
    "eswatini":                         "sz",
    "st_helena":                        "sh",
    "guinea_bissau": "gw",
}

output_dir = os.path.join(os.path.dirname(__file__), "flags")
os.makedirs(output_dir, exist_ok=True)

for name in names:
    # e.g. "cape_verde" → "Cape Verde"
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