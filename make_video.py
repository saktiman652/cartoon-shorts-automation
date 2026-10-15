
import os
import math
import wave
import glob
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

W, H = 540, 960
FPS = 12
DURATION = 30
OUT = Path("output")
FRAMES = OUT / "frames"

OUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

STORY = [
    ("एक दिन गोलू को एक जादुई खिलौना कार मिली।", "गोलू को मिली जादुई कार!"),
    ("कार का बटन दबाते ही वह चमकने लगी।", "वाह! कार चमकने लगी!"),
    ("गोलू कार लेकर अपने बगीचे में गया।", "चलो बगीचे की सैर करें!"),
    ("रास्ते में उसे एक छोटा खरगोश मिला।", "नन्हे खरगोश से मुलाकात"),
    ("गोलू ने खरगोश को भी अपनी कार में घुमाया।", "दोस्ती सबसे प्यारी है!"),
    ("दोनों खुश हुए और अच्छे दोस्त बन गए।", "खुशी बाँटने से बढ़ती है!")
]

def get_font(size):
    paths = glob.glob(
        "/usr/share/fonts/**/*Devanagari*",
        recursive=True
    )
    paths += glob.glob(
        "/usr/share/fonts/**/*NotoSans*",
        recursive=True
    )
    for path in paths:
        if path.lower().endswith((".ttf", ".otf")):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT = get_font(29)
SMALL = get_font(23)

def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        box, radius=radius, fill=fill,
        outline=outline, width=width
    )

def make_background(scene, t):
    img = Image.new("RGB", (W, H))
    pix = img.load()

    skies = [
        ((65, 160, 240), (220, 245, 255)),
        ((90, 175, 245), (245, 240, 190)),
        ((55, 155, 225), (225, 250, 210)),
        ((85, 175, 235), (255, 225, 190)),
        ((65, 150, 230), (235, 240, 255)),
        ((70, 145, 225), (255, 220, 170))
    ]
    top, bottom = skies[scene]

    for y in range(H):
        k = y / H
        c = tuple(
            int(top[i] * (1-k) + bottom[i] * k)
            for i in range(3)
        )
        for x in range(W):
            pix[x, y] = c

    d = ImageDraw.Draw(img, "RGBA")

    # Soft clouds
    for cx, cy in [(90, 150), (380, 205), (280, 100)]:
        cx = int((cx + t * 9) % (W + 100) - 40)
        d.ellipse((cx-45, cy, cx+25, cy+35),
                  fill=(255, 255, 255, 220))
        d.ellipse((cx-15, cy-20, cx+45, cy+35),
                  fill=(255, 255, 255, 235))
        d.ellipse((cx+15, cy, cx+65, cy+35),
                  fill=(255, 255, 255, 220))

    # Sun
    d.ellipse((410, 65, 485, 140), fill=(255, 220, 65, 255))
    d.ellipse((422, 77, 473, 128), fill=(255, 238, 125, 255))

    # Hills and ground
    d.ellipse((-120, 500, 350, 760), fill=(100, 205, 115, 255))
    d.ellipse((170, 485, 700, 760), fill=(65, 180, 105, 255))
    d.rectangle((0, 670, W, H), fill=(85, 190, 100, 255))

    # Small flowers
    for x in range(35, W, 95):
        y = 720 + (x % 3) * 22
        d.line((x, y, x, y+24), fill=(25, 120, 55, 255), width=3)
        d.ellipse((x-7, y-6, x+7, y+8),
                  fill=(255, 230, 65, 255))

    return img

def draw_boy(d, x, y, t):
    bob = int(math.sin(t * 5) * 5)
    y += bob

    # Ground shadow
    d.ellipse((x-55, y+165, x+60, y+185),
              fill=(35, 100, 55, 90))

    # Legs and shoes
    d.rounded_rectangle((x-31, y+100, x-8, y+158),
                        radius=10, fill=(45, 75, 180))
    d.rounded_rectangle((x+8, y+100, x+31, y+158),
                        radius=10, fill=(45, 75, 180))
    d.ellipse((x-43, y+145, x-5, y+168), fill=(255, 255, 255))
    d.ellipse((x+4, y+145, x+43, y+168), fill=(245, 245, 255))

    # Body with simple shading
    d.ellipse((x-39, y+30, x+39, y+130), fill=(30, 105, 220))
    d.ellipse((x-30, y+35, x+10, y+115), fill=(65, 150, 255))

    # Moving arms
    swing = int(math.sin(t * 5) * 12)
    d.line((x-28, y+48, x-48, y+85+swing),
           fill=(245, 190, 145), width=17)
    d.line((x+28, y+48, x+49, y+82-swing),
           fill=(245, 190, 145), width=17)

    # Head and ears
    d.ellipse((x-39, y-45, x-16, y-10), fill=(245, 190, 145))
    d.ellipse((x+16, y-45, x+39, y-10), fill=(245, 190, 145))
    d.ellipse((x-43, y-65, x+43, y+22), fill=(245, 190, 145))
    d.ellipse((x-38, y-62, x+28, y+12), fill=(255, 210, 165))

    # Hair
    d.ellipse((x-43, y-75, x+35, y-32), fill=(65, 35, 25))
    d.ellipse((x-35, y-85, x-5, y-48), fill=(75, 40, 25))
    d.ellipse((x-8, y-83, x+24, y-48), fill=(65, 35, 25))

    # Eyes and smile
    d.ellipse((x-25, y-25, x-12, y-8), fill="white")
    d.ellipse((x+12, y-25, x+25, y-8), fill="white")
    d.ellipse((x-20, y-21, x-13, y-10), fill=(35, 35, 45))
    d.ellipse((x+14, y-21, x+21, y-10), fill=(35, 35, 45))
    d.arc((x-17, y-8, x+18, y+13), 5, 165,
          fill=(145, 45, 40), width=3)

def draw_car(d, x, y, t):
    bounce = int(math.sin(t * 7) * 3)
    y += bounce

    # Shadow
    d.ellipse((x-75, y+35, x+85, y+58),
              fill=(30, 100, 45, 90))

    # Car body
    d.rounded_rectangle((x-83, y-5, x+83, y+40),
                        radius=15, fill=(220, 35, 55))
    d.rounded_rectangle((x-48, y-37, x+38, y+5),
                        radius=15, fill=(245, 65, 75))
    d.polygon([(x-36, y-30), (x-5, y-30),
               (x-5, y-3), (x-48, y-3)],
              fill=(150, 225, 255))
    d.polygon([(x+2, y-30), (x+29, y-30),
               (x+34, y-3), (x+2, y-3)],
              fill=(170, 235, 255))

    # Highlight
    d.line((x-65, y+2, x+58, y+2),
           fill=(255, 130, 130), width=5)

    # Wheels
    for wx in (x-48, x+48):
        d.ellipse((wx-20, y+22, wx+20, y+62),
                  fill=(35, 40, 55))
        d.ellipse((wx-10, y+32, wx+10, y+52),
                  fill=(200, 215, 225))
        d.ellipse((wx-4, y+38, wx+4, y+46),
                  fill=(100, 115, 130))

def draw_rabbit(d, x, y):
    d.ellipse((x-35, y-55, x-10, y+5), fill=(250, 250, 250))
    d.ellipse((x+10, y-55, x+35, y+5), fill=(250, 250, 250))
    d.ellipse((x-29, y-45, x-17, y-5), fill=(245, 145, 165))
    d.ellipse((x+17, y-45, x+29, y-5), fill=(245, 145, 165))
    d.ellipse((x-38, y-10, x+38, y+65), fill=(250, 250, 250))
    d.ellipse((x-30, y+45, x-5, y+67), fill=(255, 255, 255))
    d.ellipse((x+5, y+45, x+30, y+67), fill=(255, 255, 255))
    d.ellipse((x-22, y+8, x-12, y+20), fill=(40, 40, 40))
    d.ellipse((x+12, y+8, x+22, y+20), fill=(40, 40, 40))
    d.ellipse((x-5, y+23, x+5, y+31), fill=(240, 130, 150))

def add_caption(img, text):
    d = ImageDraw.Draw(img, "RGBA")
    box = (20, 795, W-20, 910)
    rounded(d, box, 24, (15, 25, 55, 205))
    d.rounded_rectangle((28, 803, W-28, 810),
                        radius=3, fill=(255, 210, 55, 255))

    # Center the Hindi text
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if d.textbbox((0, 0), test, font=FONT)[2] > W-65:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)

    yy = 830
    for line in lines[:2]:
        bbox = d.textbbox((0, 0), line, font=FONT)
        xx = (W - (bbox[2]-bbox[0])) // 2
        d.text((xx+2, yy+3), line, font=FONT, fill=(0, 0, 0, 180))
        d.text((xx, yy), line, font=FONT, fill=(255, 255, 255, 255))
        yy += 38

def create_frames():
    for i in range(FPS * DURATION):
        t = i / FPS
        scene = min(int(t // 5), 5)
        local_t = t - scene * 5

        img = make_background(scene, local_t)
        d = ImageDraw.Draw(img, "RGBA")

        # A consistent character and toy car in every scene
        bx = 180 + int(math.sin(local_t * 1.5) * 12)
        draw_boy(d, bx, 525, local_t)

        car_x = 350 + int(math.sin(local_t * 2) * 18)
        draw_car(d, car_x, 650, local_t)

        # The rabbit joins the story in later scenes
        if scene >= 3:
            draw_rabbit(d, 425, 565)

        # Sparkles for a magical feel
        if scene in (0, 1, 4):
            for sx, sy in [(95, 400), (425, 380), (290, 470)]:
                pulse = int(4 * math.sin(t * 5))
                r = 7 + pulse
                d.ellipse((sx-r, sy-r, sx+r, sy+r),
                          fill=(255, 235, 90, 230))
                d.line((sx-13, sy, sx+13, sy),
                       fill=(255, 255, 210, 230), width=2)
                d.line((sx, sy-13, sx, sy+13),
                       fill=(255, 255, 210, 230), width=2)

        add_caption(img, STORY[scene][1])

        # Intro title at the top
        rounded(d, (25, 25, W-25, 78), 18, (20, 55, 110, 175))
        title = "गोलू और जादुई कार"
        bbox = d.textbbox((0, 0), title, font=SMALL)
        d.text(((W-(bbox[2]-bbox[0]))//2, 38),
               title, font=SMALL, fill=(255, 255, 255, 255))

        img.save(FRAMES / f"frame_{i:04d}.png")

def create_music():
    # Original soft synthesized background melody
    sr = 22050
    total = sr * DURATION
    notes = [261.63, 329.63, 392.00, 329.63,
             293.66, 349.23, 440.00, 349.23]
    audio = np.zeros(total, dtype=np.float32)

    for i, start in enumerate(range(0, total, sr)):
        end = min(start + sr, total)
        n = end - start
        t = np.arange(n) / sr
        freq = notes[i % len(notes)]
        tone = (
            0.55 * np.sin(2 * np.pi * freq * t) +
            0.20 * np.sin(2 * np.pi * freq * 2 * t)
        )
        fade = np.minimum(1, t * 4)
        fade *= np.minimum(1, (n / sr - t) * 4)
        audio[start:end] += 0.10 * tone * fade

    audio = np.clip(audio, -0.8, 0.8)
    stereo = np.column_stack((audio, audio))
    pcm = (stereo * 32767).astype(np.int16)

    with wave.open(str(OUT / "background-music.wav"), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(pcm.tobytes())

def main():
    narration = " ".join(item[0] for item in STORY)
    voice_path = OUT / "hindi-narration.mp3"

    print("Creating Hindi narration...")
    gTTS(text=narration, lang="hi", slow=False).save(str(voice_path))

    print("Creating original background music...")
    create_music()

    print("Drawing cartoon animation...")
    create_frames()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is not installed")

    output_file = OUT / "cartoon-video.mp4"
    command = [
        ffmpeg, "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES / "frame_%04d.png"),
        "-i", str(voice_path),
        "-i", str(OUT / "background-music.wav"),
        "-filter_complex",
        "[1:a]volume=1.0[voice];"
        "[2:a]volume=0.18[music];"
        "[voice][music]amix=inputs=2:duration=longest:"
        "dropout_transition=2[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-t", str(DURATION),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=720:1280",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        str(output_file)
    ]

    print("Rendering final vertical video...")
    subprocess.run(command, check=True)

    print(f"SUCCESS: Video saved to {output_file}")

if __name__ == "__main__":
    main()
