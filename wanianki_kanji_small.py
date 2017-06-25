# Smaller version (for my iPhone SE screen)
# Uses:
#   genanki: https://github.com/kerrickstaley/genanki
#   kanji stroke order font: http://www.nihilist.org.uk/
#   Pillow: https://python-pillow.org/

import random
import genanki
import json
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image


# If you plan to use this script multiple times to update decks, hardcode the model IDs below -- they're unique
# IDs for your model and deck respectively.
kanji_model_id = random.randrange(1 << 30, 1 << 31)
wanianki_kanji_id = random.randrange(1 << 30, 1 << 31)

kanji_model = genanki.Model(kanji_model_id, 'Kanji Model',
    fields=[
        {'name': 'Kanji'},
        {'name': 'Meaning'},
        {'name': 'Onyomi'},
        {'name': 'Kunyomi'},
        {'name': 'Nanori'},
        {'name': 'Reading'},
        {'name': 'Level'},
        {'name': 'KanjiID'},
    ],
    templates=[
        {
            'name': 'WaniAnki Kanji',
            'qfmt': '<div class="style-level">L{{Level}}</div>'
                    '<div class="style-front">{{Kanji}}</div>',
            'afmt': '<div class="style-level">L{{Level}}</div>'
                    '<img src="{{KanjiID}}.png">'
                    '<div class="line-dash"></div>'
                    '<p class="style-meaning">{{Meaning}}</p>'
                    '<p class="style-reading">{{Reading}}</p>'
                    '<p class="style-others">Onyomi: {{Onyomi}}</p>'
                    '<p class="style-others">Kunyomi: {{Kunyomi}}</p>'
                    '<p class="style-others">Nanori: {{Nanori}}</p>',
        },
    ],
    css=".card { text-align:center; color: #ffffff; background: #f100a1; margin: 5px auto; }"
        ".style-front { text-align:center; font-size: 115px; color: #ffffff; background: #f100a1; margin-top: 5px; }"
        ".style-meaning { text-align:center; font-size: 25px; color: #ffffff; background: #f100a1; margin: 0px; }"
        ".style-level { font-size: 10px; font-weight: bold; position: absolute; top: 0; right: 0; margin: 5px; }"
        ".style-reading { text-align:center; font-size: 30px; color: #ffffff; background: #f100a1; margin-top: 10px; margin-bottom: 10px; } "
        ".style-others { font-size: 15px; color: #ffffff; text-align: center; margin: 0px; padding: 0px; } "
        ".line-dash { margin-top: 5px; margin-bottom: 15px;  border-top: #ffffff dashed 2px; }")

wanianki_kanji = genanki.Deck(wanianki_kanji_id, 'WaniAnki Kanji')

kanji_character = []
kanji_onyomi = []
kanji_kunyomi = []
kanji_nanori = []
kanji_reading = []
kanji_level = []

kid = 1

with open('wanikani_kanji.json') as kanji:
    font = ImageFont.truetype("KanjiStrokeOrders_v4.001.ttf", 150)
    k = json.load(kanji)
    sortlevel = [x for x in k['requested_information'] if 'level' in x]
    kanji_by_level = sorted(sortlevel, key=lambda x: x['level'])

    for kan in kanji_by_level:
        kanji_character = kan['character']
        img = Image.new("RGB", (200, 200), (241, 0, 161))
        draw = ImageDraw.Draw(img)
        draw.text((20, 0), kanji_character, (255, 255, 255), font=font)
        draw = ImageDraw.Draw(img)
        img.save(str(kid) + ".png")

        kanji_meaning = kan['meaning']
        if kan['onyomi']:
            kanji_onyomi = kan['onyomi']
        else:
            kanji_onyomi = "None"
        if kan['nanori']:
            kanji_nanori = kan['nanori']
        else:
            kanji_nanori = "None"
        if kan['kunyomi']:
            kanji_kunyomi = kan['kunyomi']
        else:
            kanji_kunyomi = "None"

        kanji_reading = kan['important_reading']
        kanji_level = str(kan['level'])
        save_kid = str(kid)
        print('Building reverse card ' + save_kid + ', level ' + kanji_level + ': ' + kanji_character)
        if kanji_reading == 'onyomi':
            new_note = genanki.Note(model=kanji_model, fields=[kanji_character, kanji_meaning, kanji_onyomi, kanji_kunyomi, kanji_nanori, kanji_onyomi, kanji_level, save_kid])
            wanianki_kanji.add_note(new_note)
        elif kanji_reading == 'kunyomi':
            new_note = genanki.Note(model=kanji_model, fields=[kanji_character, kanji_meaning, kanji_onyomi, kanji_kunyomi, kanji_nanori, kanji_kunyomi, kanji_level, save_kid])
            wanianki_kanji.add_note(new_note)
        elif kanji_reading == 'nanori':
            new_note = genanki.Note(model=kanji_model, fields=[kanji_character, kanji_meaning, kanji_onyomi, kanji_kunyomi, kanji_nanori, kanji_kunyomi, kanji_level, save_kid])
            wanianki_kanji.add_note(new_note)
        kid += 1

kanji_media_files = []
kid_range = range(1, kid)
for i in kid_range:
    kanji_media_files.append(str(i) + '.png')

wanikani_kanji_package = genanki.Package(wanianki_kanji)
wanikani_kanji_package.media_files = kanji_media_files
wanikani_kanji_package.write_to_file('wanikani_kanji.apkg')
