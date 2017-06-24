# Smaller version (for my iPhone SE screen)
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
        {'name': 'VocabIDR'},
        {'name': 'VocabularyR'},
        {'name': 'KanaR'},
        {'name': 'MeaningR'},
        {'name': 'LevelR'},
    ],
    templates=[
        {
            'name': 'WaniAnki Vocabulary Reverse',
            'qfmt': '<div class="style-level">L{{LevelR}}</div>'
                    '<div class="style-front">{{MeaningR}}</div>',
            'afmt': '<div class="style-level">L{{LevelR}}</div>'
                    '<div class="style-front">{{MeaningR}}</div>'
                    '<div class="line-dash"></div>'
                    '<img src="v{{VocabIDR}}.png">'
                    '<p class="style-reading">{{KanaR}}</p>',
        },
    ],
    css=".card { text-align:center; font-size: 40px; color: #ffffff; background: #a100f1; margin: 25px auto; }"
        ".style-front { text-align:center; font-size: 40px; color: #ffffff; background: #a100f1; }"
        ".style-level { font-size: 10px; font-weight: bold; position: absolute; top: 0; right: 0; margin: 5px; }"
        ".style-reading { text-align:center; font-size: 50px; color: #ffffff; background: #a100f1; margin-top: 5px; } "
        ".line-dash { margin-top: 30px; margin-bottom: 10px; border-top: #ffffff dashed 2px; }")

wanianki_vocabulary_reverse = genanki.Deck(wanianki_vocabulary_reverse_id, 'WaniAnki Vocabulary Reverse')

vocabularyR = []
vocabulary_kanaR = []
vocabulary_meaningR = []
vocabulary_levelR = []

vidR = 1
maxlength = 0

with open('wanikani_vocabulary.json') as vocab:
    font = ImageFont.truetype("KanjiStrokeOrders_v4.001.ttf", 100)
    v = json.load(vocab)
    sortlevel = [x for x in v['requested_information'] if 'level' in x]
    vocab_by_level = sorted(sortlevel, key=lambda x: x['level'])

    for voc in vocab_by_level:
        vocabularyR = voc['character']
        charlength = len(vocabularyR)
        width = (charlength * 103) + (50 - (charlength * 5))
        img = Image.new("RGB", (width, 140), (161, 0, 241))
        draw = ImageDraw.Draw(img)
        draw.text((20, 0), vocabularyR, (255, 255, 255), font=font)
        draw = ImageDraw.Draw(img)
        img.save('v' + str(vidR) + 'R.png')
        vocabulary_kanaR = voc['kana']
        vocabulary_meaningR = voc['meaning']
        vocabulary_levelR = str(voc['level'])
        save_vidR = str(vidR)
        print('Building reverse card ' + save_vidR + ', level ' + vocabulary_levelR + ': ' + vocabularyR)
        new_note_reverse = genanki.Note(model=vocabulary_reverse_model, fields=[save_vidR, vocabularyR, vocabulary_kanaR, vocabulary_meaningR, vocabulary_levelR])
        wanianki_vocabulary_reverse.add_note(new_note_reverse)
        vidR += 1

vocab_media_filesR = []
vid_rangeR = range(1, vidR)
for i in vid_rangeR:
    vocab_media_filesR.append('v' + str(i) + 'R.png')
wanianki_vocabulary_reverse_package = genanki.Package(wanianki_vocabulary_reverse)
wanianki_vocabulary_reverse_package.media_files = vocab_media_filesR
wanianki_vocabulary_reverse_package.write_to_file('wanikani_vocabulary_reverse.apkg')
