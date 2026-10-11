

from datetime import date
from pathlib import Path
import random

TOPICS = [
    {
        "title": "Golu Aur Gum Hua Khilona",
        "story": "Golu bhalu apne dost ka khoya khilona dhoondhta hai.",
        "character": (
            "Golu: a cute small honey-brown bear, round face, "
            "cream muzzle, big brown eyes, tiny round ears, "
            "red T-shirt, blue shorts, small green backpack"
        ),
        "scenes": [
            "Golu smiles at the camera and suddenly notices an empty toy box.",
            "Golu's little rabbit friend looks sad because his yellow toy car is missing.",
            "Golu searches beside a tree and discovers the yellow car behind a bush.",
            "Golu returns the car to his happy rabbit friend. They celebrate together."
        ],
        "voice": [
            "Golu ko aaj ek ajeeb cheez dikhi!",
            "Uske dost ki pyari khilona gaadi kho gayi thi.",
            "Golu ne har jagah dhoonda aur gaadi mil gayi!",
            "Dost khush ho gaya. Saccha dost wahi jo madad kare!"
        ]
    },
    {
        "title": "Chhote Bunny Ki Madad",
        "story": "Ek chhota bunny raste mein gire hue chuze ki madad karta hai.",
        "character": (
            "Bunny: a tiny white rabbit, pink inner ears, "
            "large blue eyes, yellow overalls, orange shoes"
        ),
        "scenes": [
            "Bunny hops along a colorful garden path and hears a tiny chirp.",
            "A little yellow chick is stuck beside a small puddle.",
            "Bunny carefully helps the chick onto dry grass.",
            "The chick happily follows Bunny through the sunny garden."
        ],
        "voice": [
            "Bunny ko achanak ek awaaz sunai di!",
            "Ek nanha chuza raste mein phans gaya tha.",
            "Bunny ne pyaar se uski madad ki.",
            "Chuza khush ho gaya. Madad karna achhi baat hai!"
        ]
    },
    {
        "title": "Mimi Ki Jadui Pencil",
        "story": "Ek pyari billi ki pencil se banayi cheezein sach ho jaati hain.",
        "character": (
            "Mimi: a tiny fluffy white kitten, blue eyes, "
            "pink nose, purple dress, small yellow hair bow"
        ),
        "scenes": [
            "Mimi discovers a sparkling pencil on her colorful desk.",
            "She draws a tiny butterfly, which magically comes alive.",
            "Mimi draws a flower and watches it bloom beside her.",
            "Mimi shares her magical drawings with her delighted friends."
        ],
        "voice": [
            "Mimi ko mili ek chamakti jadui pencil!",
            "Usne titli banayi aur woh sach mein udne lagi!",
            "Phir usne ek sundar phool bana diya.",
            "Mimi ne apna jaadu sabke saath baanta!"
        ]
    },
    {
        "title": "Nanhe Haathi Ka Birthday",
        "story": "Ek nanha haathi apne dost ke liye surprise birthday party banata hai.",
        "character": (
            "A tiny cute gray elephant, large floppy ears, "
            "short trunk, big brown eyes, blue overalls, "
            "yellow party hat"
        ),
        "scenes": [
            "The little elephant looks at a calendar and gets a fun idea.",
            "His friend feels sad because nobody seems to remember his birthday.",
            "The elephant decorates a garden with balloons and a cake.",
            "His friend arrives and everyone celebrates a happy birthday."
        ],
        "voice": [
            "Nanhe haathi ke dimaag mein aaya ek idea!",
            "Uske dost ko laga sab uska birthday bhool gaye.",
            "Haathi ne chupke se party taiyar kar di.",
            "Surprise! Sabne milkar birthday manaya!"
        ]
    },
    {
        "title": "Chidiya Ka Chhota Ghar",
        "story": "Ek bachcha aur ek chidiya toofan ke baad ghar banate hain.",
        "character": (
            "A tiny bright-yellow bird, orange beak, "
            "round body, big black eyes, little blue scarf; "
            "a kind young child wearing green overalls"
        ),
        "scenes": [
            "A little yellow bird looks sadly at its damaged nest.",
            "A kind child notices the bird and decides to help.",
            "Together they collect twigs and soft leaves for a new nest.",
            "The bird rests safely in its new nest as the child smiles."
        ],
        "voice": [
            "Chidiya ka chhota sa ghar toot gaya!",
            "Ek bachche ne uski udaasi dekh li.",
            "Dono ne milkar naya ghar banaya.",
            "Ab chidiya surakshit thi aur dono khush the!"
        ]
    }
]

topic = random.choice(TOPICS)
today = date.today().isoformat()

brief = f"""# Daily 3D Cartoon Short
Date: {today}

## Story
{topic['title']}

{topic['story']}

## Video Settings
- Duration: 30-40 seconds
- Format: vertical 9:16
- Style: colorful, high-quality, child-friendly 3D animation
- Language: simple Hindi
- No scary scenes or violence

## Character Reference
Create a reference image before generating scenes.

CHARACTER LOCK:
{topic['character']}

Keep the exact same face, colors, clothes, accessories,
body proportions and animation style in every scene.
Use the same reference image in every scene whenever supported.
Do not redesign, recolor or replace the characters.

## Scene-by-Scene Prompts

"""

durations = ["0-5 sec", "5-15 sec", "15-28 sec", "28-40 sec"]

for i, (scene, voice, duration) in enumerate(
    zip(topic["scenes"], topic["voice"], durations), start=1
):
    brief += f"""### Scene {i}: {duration}

Visual: {scene}

Character consistency: {topic['character']}

Generation prompt:
Create a colorful, polished 3D animated children's cartoon.
Vertical 9:16 composition. {scene}
Maintain the exact character designs described above.
Use expressive faces, smooth animation, bright lighting,
clear actions and a child-friendly environment.
No character redesign, no costume changes, no watermark.

Hindi voiceover:
{voice}

Sound: gentle, cheerful background music and suitable
soft sound effects. Keep dialogue clear.

"""

brief += f"""## Video Assembly
- Arrange scenes in order.
- Total target duration: 30-40 seconds.
- Add Hindi voiceover and synchronize it with the action.
- Use smooth transitions and readable Hindi subtitles.
- Export vertical 1080x1920 MP4 at 30 fps.
- Check the complete video before publishing.

## YouTube Title
{topic['title']} | Hindi 3D Cartoon Short #Shorts

## Description
{topic['story']}
Ek pyari si Hindi cartoon kahani bachchon ke liye.
Video pasand aaye to like aur subscribe karein.

## Hashtags
#Shorts #3DCartoon #HindiKahani
#KidsAnimation #CartoonShorts

## Upload Checklist
- Check character consistency in all scenes.
- Check Hindi voiceover and subtitles.
- Use music and sound effects you have permission to use.
- Review the final video before uploading.
- Upload only after checking the title, description and audience settings.
"""

Path("output").mkdir(exist_ok=True)
Path("output/daily-brief.md").write_text(brief, encoding="utf-8")

print("Daily cartoon brief created:", topic["title"])

