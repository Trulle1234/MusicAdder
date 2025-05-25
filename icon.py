# pip install pillow

import os
from PIL import Image

# Paths – adjust to your layout
project_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(project_dir, "music_disc_template.png")
flags_dir     = os.path.join(project_dir, "flags")
output_dir    = os.path.join(project_dir, "generated_textures")
os.makedirs(output_dir, exist_ok=True)

# Load your 16×16 disc template (must be RGBA)
template = Image.open(template_path).convert("RGBA")
W, H = template.size
assert (W, H) == (16, 16), "Template must be 16×16px!"

# Detect transparent hole bounding box and its center
min_x, min_y = W, H
max_x = max_y = 0
for y in range(H):
    for x in range(W):
        if template.getpixel((x, y))[3] == 0:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
hole_cx = (min_x + max_x) / 2
hole_cy = (min_y + max_y) / 2

for fname in os.listdir(flags_dir):
    if not fname.lower().endswith(".png"):
        continue

    country = os.path.splitext(fname)[0]
    flag = Image.open(os.path.join(flags_dir, fname)).convert("RGBA")

    # 1) Resize flag to exactly 7×5
    flag_small = flag.resize((7, 5), Image.LANCZOS)

    # 2) Quantize only the flag_small RGB to 5 colors
    rgb = flag_small.convert("RGB")
    quantized_rgb = rgb.quantize(colors=5, method=Image.MEDIANCUT).convert("RGB")
    alpha = flag_small.getchannel("A")
    flag_small = Image.merge("RGBA", (*quantized_rgb.split(), alpha))

    # 3) Compute paste coords to center flag behind hole
    paste_x = int(hole_cx - flag_small.width / 2)
    paste_y = int(hole_cy - flag_small.height / 2)

    # 4) Create blank RGBA canvas and paste the quantized flag
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.paste(flag_small, (paste_x, paste_y), flag_small)

    # 5) Composite disc template on top so the flag sits behind the opaque areas
    composed = Image.alpha_composite(base, template)

    # 6) Save out final image
    out_path = os.path.join(output_dir, f"music_disc_{country}.png")
    composed.save(out_path)

    print(f"✓ music_disc_{country}.png (flag quantized to 5 colors)")