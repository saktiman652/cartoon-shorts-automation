
from pathlib import Path
import subprocess
import shutil
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
FPS = 24
SCENE_SECONDS = 5
OUT = Path("output")
SCENES = OUT / "scenes"

OUT.mkdir(exist_ok=True)
SCENES.mkdir(exist_ok=True)

# Hindi font installed by the GitHub Actions workflow
FONT_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

def get_font(size):
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

title_font = get_font(48)
caption_font = get_font(39)
small_font = get_font(27)

scenes = [
    ("अरे! गोलू का खिलौना कहाँ गया?", "एक सुबह गोलू का प्यारा खिलौना गायब था!", (255, 215, 110)),
    ("गोलू ने कमरा देखा", "उसने मेज और बिस्तर के नीचे ढूँढा।", (160, 220, 255)),
    ("फिर भी नहीं मिला!", "गोलू थोड़ा उदास हो गया।", (255, 180, 190)),
    ("तभी कुछ चमका!", "पर्दे के पीछे उसे एक छोटा पहिया दिखा।", (190, 240, 180)),
    ("मिल गया खिलौना!", "खिलौना सोफे के पीछे छिपा था।", (220, 190, 255)),
    ("गोलू खुशी से हँसा!", "सीख: किसी चीज़ को ढूँढते समय हार मत मानो।", (255, 225, 140)),
]

def centered(draw, text, y, font, fill, max_width=650):
    # Wrap text into short lines that fit the vertical video
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    for item in lines:
        box = draw.textbbox((0, 0), item, font=font, stroke_width=1)
        x = (W - (box[2] - box[0])) // 2
        draw.text(
            (x, y), item, font=font, fill=fill,
            stroke_width=1, stroke_fill=(40, 40, 60)
        )
        y += font.size + 12
    return y

def draw_scene(index, headline, caption, bg):
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)

    # Decorative clouds
    d.ellipse((40, 130, 190, 210), fill=(255, 255, 255))
    d.ellipse((95, 105, 235, 205), fill=(255, 255, 255))
    d.ellipse((510, 170, 660, 240), fill=(255, 255, 255))

    # Floor
    d.rectangle((0, 920, W, H), fill=(115, 195, 115))

    # Cartoon character: same design in every scene
    # Head, ears, hair, eyes, smile, body and blue trousers
    d.ellipse((260, 385, 460, 585), fill=(255, 190, 135),
              outline=(100, 65, 55), width=5)
    d.ellipse((244, 450, 280, 510), fill=(255, 190, 135),
              outline=(100, 65, 55), width=4)
    d.ellipse((440, 450, 476, 510), fill=(255, 190, 135),
              outline=(100, 65, 55), width=4)
    d.pieslice((255, 360, 465, 500), 180, 360,
               fill=(80, 45, 30), outline=(80, 45, 30))
    d.ellipse((305, 455, 330, 485), fill=(40, 40, 50))
    d.ellipse((385, 455, 410, 485), fill=(40, 40, 50))
    d.arc((325, 475, 390, 535), 10, 160, fill=(140, 40, 45), width=5)

    # Red shirt and blue trousers
    d.rounded_rectangle((260, 570, 460, 800), radius=45,
                        fill=(235, 65, 75), outline=(100, 40, 50), width=5)
    d.rectangle((295, 770, 345, 910), fill=(50, 95, 210))
    d.rectangle((375, 770, 425, 910), fill=(50, 95, 210))
    d.ellipse((280, 880, 355, 930), fill=(80, 50, 35))
    d.ellipse((365, 880, 440, 930), fill=(80, 50, 35))

    # Toy car appears in the later scenes
    if index >= 3:
        d.rounded_rectangle((460, 790, 625, 875), radius=20,
                            fill=(255, 205, 45),
                            outline=(100, 70, 25), width=5)
        d.polygon([(485, 790), (520, 740), (570, 740), (605, 790)],
                  fill=(255, 205, 45), outline=(100, 70, 25))
        d.ellipse((480, 850, 525, 895), fill=(45, 45, 55))
        d.ellipse((565, 850, 610, 895), fill=(45, 45, 55))
        d.ellipse((491, 861, 514, 884), fill=(230, 230, 230))
        d.ellipse((576, 861, 599, 884), fill=(230, 230, 230))

    # Text panels
    d.rounded_rectangle((25, 20, 695, 330), radius=35,
                        fill=(255, 255, 255), outline=(70, 70, 90), width=4)
    centered(d, headline, 55, title_font, (45, 45, 90))
    centered(d, caption, 190, caption_font, (55, 55, 65))

    # Scene number
    d.rounded_rectangle((270, 1160, 450, 1220), radius=25,
                        fill=(255, 255, 255))
    label = f"सीन {index + 1} / 6"
    box = d.textbbox((0, 0), label, font=small_font)
    d.text(((W - (box[2] - box[0])) // 2, 1175),
           label, font=small_font, fill=(40, 60, 80))

    return im

for i, (headline, caption, bg) in enumerate(scenes):
    image = draw_scene(i, headline, caption, bg)
    image.save(SCENES / f"scene_{i:02d}.png")

ffmpeg = shutil.which("ffmpeg")
if not ffmpeg:
    raise RuntimeError("FFmpeg is missing. Install it in the GitHub Actions workflow.")

# Create a video from six 5-second scenes.
concat_file = OUT / "scenes.txt"
with concat_file.open("w", encoding="utf-8") as f:
    for i in range(len(scenes)):
        f.write(f"file 'scenes/scene_{i:02d}.png'\n")
        f.write(f"duration {SCENE_SECONDS}\n")
    # Repeat final frame so FFmpeg honors its duration
    f.write(f"file 'scenes/scene_{len(scenes)-1:02d}.png'\n")

video_path = OUT / "cartoon-video.mp4"
subprocess.run([
    ffmpeg, "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(concat_file),
    "-vf", f"fps={FPS},scale={W}:{H},format=yuv420p",
    "-t", str(len(scenes) * SCENE_SECONDS),
    "-movflags", "+faststart",
    str(video_path),
], check=True)

print(f"Video created: {video_path}")
