
from datetime import date
from pathlib import Path
import random

TOPICS = [
    {
        "title": "Chhote Bunny Ki Madad",
        "story": "Ek chhota bunny raste mein gire hue chuze ki madad karta hai."
    },
    {
        "title": "Mimi Ki Jadui Pencil",
        "story": "Ek pyari billi ki pencil se banayi cheezein sach ho jaati hain."
    },
    {
        "title": "Nanhe Haathi Ka Birthday",
        "story": "Ek nanha haathi apne dost ke liye surprise birthday party banata hai."
    },
    {
        "title": "Golu Aur Gum Hua Khilona",
        "story": "Ek chhota bhalu apne dost ka khoya khilona dhoondhta hai."
    },
    {
        "title": "Chidiya Ka Chhota Ghar",
        "story": "Ek bachcha aur ek chidiya milkar toofan ke baad ghar banate hain."
    },
]

topic = random.choice(TOPICS)
today = date.today().isoformat()

brief = f"""# Daily 3D Cartoon Short
Date: {today}

## Story
{topic['title']}

{topic['story']}

## Video requirements
- Duration: 30–40 seconds
- Format: vertical 9:16
- Style: colorful, child-friendly 3D animation
- Language: simple Hindi
- Structure: hook, problem, solution, happy ending

## Character consistency
Create a character reference image first.
Keep the exact same face, colors, body proportions,
clothes and accessories in every scene.
Reuse the same reference image whenever supported.

## Scene prompts
1. 0–5 sec: Show the main character and an interesting hook.
2. 5–15 sec: Introduce the small problem.
3. 15–28 sec: Show the character trying to solve it.
4. 28–40 sec: Show the solution and a happy ending.

## Title
{topic['title']} | Hindi 3D Cartoon Short #Shorts

## Description
Ek pyari si Hindi cartoon kahani bachchon ke liye.
Video pasand aaye to like aur subscribe karein.

## Hashtags
#Shorts #3DCartoon #HindiKahani
#KidsAnimation #CartoonShorts

## Before upload
- Generate visuals and edit the video.
- Check that all scenes use the same character design.
- Use only music and sound effects you have permission to use.
- Watch the final video before uploading.
"""

Path("output").mkdir(exist_ok=True)
Path("output/daily-brief.md").write_text(brief, encoding="utf-8")
print("Daily content brief created:", topic["title"])
