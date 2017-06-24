# English meaning on front, kanji/reading/stroke order on back
#
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
wanianki_vocabulary_reverse_id = random.randrange(1 << 30, 1 << 31)
vocabulary_reverse_model_id = random.randrange(1 << 30, 1 << 31)

vocabulary_reverse_model = genanki.Model(vocabulary_reverse_model_id, 'Vocabulary Reverse Model',
    fields=[
        {'name': 'Vocabulary'},
        {'name': 'Kana'},
        {'name': 'Meaning'},
        {'name': 'Level'},
        {'name': 'VocabID'},
    ],
    templates=[
        {
            'name': 'WaniAnki Vocabulary Reverse',
            'qfmt': '<div class="style-level">Level {{Level}}</div>'
                    '<div class="style-front">{{Meaning}}</div>',
            'afmt': '<div class="style-level">Level {{Level}}</div>'
                    '<div class="style-front">{{Meaning}}</div>'
                    '<div class="line-dash"></div>'
                    '<img src="v{{VocabID}}.png">'
                    '<p class="style-reading">{{Kana}}</p>',
        },
    ],
    css=".card { font-family: Noto Sans CJK JP Regular; text-align:center; font-size: 80px; color: #ffffff; background: #a100f1; margin: 45px auto; }"
        ".style-front { font-family: Noto Sans CJK JP Regular; text-align:center; font-size: 80px; color: #ffffff; background: #a100f1; margin: 50px auto; }"
        ".style-meaning { font-family: Noto Sans CJK JP Regular; text-align:center; font-size: 50px; color: #ffffff; background: #a100f1; margin: 0px; }"
        ".style-level { font-size: 10px; font-weight: bold; position: absolute; top: 0; right: 0; margin: 15px; }"
        ".style-reading { font-family: Noto Sans CJK JP Regular; text-align:center; font-size: 60px; color: #ffffff; background: #a100f1; margin-top: 15px; margin-bottom: 25px; } "
        ".line-dash { margin: 50px; border-top: #ffffff dashed 2px; }")

wanianki_vocabulary_reverse = genanki.Deck(wanianki_vocabulary_reverse_id, 'WaniAnki Vocabulary')

vocabulary = []
vocabulary_kana = []
vocabulary_meaning = []
vocabulary_level = []

vid = 1
maxlength = 0

with open('wanikani_vocabulary.json') as vocab:
    # font = ImageFont.truetype("KanjiStrokeOrders_v4.001.ttf", 100)
    v = json.load(vocab)
    sortlevel = [x for x in v['requested_information'] if 'level' in x]
    vocab_by_level = sorted(sortlevel, key=lambda x: x['level'])

    for voc in vocab_by_level:
        vocabulary = voc['character']
        charlength = len(vocabulary)
        # width = (charlength * 103) + (50 - (charlength * 5))
        # img = Image.new("RGB", (width, 140), (161, 0, 241))
        # draw = ImageDraw.Draw(img)
        # draw.text((20, 0), vocabulary, (255, 255, 255), font=font)
        # draw = ImageDraw.Draw(img)
        # img.save('v' + str(vid) + '.png')
        vocabulary_kana = voc['kana']
        vocabulary_meaning = voc['meaning']
        vocabulary_level = str(voc['level'])
        save_vid = str(vid)
        print('Building reverse card ' + save_vid + ', level ' + vocabulary_level + ': ' + vocabulary)
        new_note_reverse = genanki.Note(model=vocabulary_reverse_model, fields=[vocabulary, vocabulary_kana, vocabulary_meaning, vocabulary_level, save_vid])
        wanianki_vocabulary_reverse.add_note(new_note_reverse)
        vid += 1

vocab_media_files = []
vid_range = range(1, vid)
for i in vid_range:
    vocab_media_files.append('v' + str(i) + '.png')
wanianki_vocabulary_reverse_package = genanki.Package(wanianki_vocabulary_reverse)
wanianki_vocabulary_reverse_package.media_files = vocab_media_files
wanianki_vocabulary_reverse_package.write_to_file('wanikani_vocabulary_reverse.apkg')
