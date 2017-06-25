# Small version (for my iPhone SE screen); combines all 3 types (kanji, vocabulary, and vocab reverse)
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
vocabulary_model_id = random.randrange(1 << 30, 1 << 31)
vocabulary_reverse_model_id = random.randrange(1 << 30, 1 << 31)
wanianki_kanji_and_vocab_id = random.randrange(1 << 30, 1 << 31)

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
            'qfmt': '<div class="style-level">Level {{Level}}</div>'
                    '<div class="style-front">{{Kanji}}</div>',
            'afmt': '<div class="style-level">Level {{Level}}</div>'
                    '<img src="{{KanjiID}}.png">'
                    '<div class="line-dash"></div>'
                    '<p class="style-meaning">{{Meaning}}</p>'
                    '<p class="style-reading">{{Reading}}</p>'
                    '<p class="style-others">Onyomi: {{Onyomi}}</p>'
                    '<p class="style-others">Kunyomi: {{Kunyomi}}</p>'
                    '<p class="style-others">Nanori: {{Nanori}}</p>',
        },
    ],
    css=".card { position: relative; text-align:center; color: #ffffff; background: #f100a1; margin: 0px auto; padding: 0px; }"
        ".style-front { font-size: 115px; margin: 0px auto; padding-top: 15px; }"
        ".style-meaning { font-size: 20px; margin: 0px auto; padding-top: 15px;}"
        ".style-level { font-size: 10px; font-weight: bold; position: absolute; top: 0; right: 0; margin: 0px; padding: 0px; }"
        ".style-reading { font-size: 25px; margin: 0px auto; padding: 15px 0px; }"
        ".style-others { font-size: 15px; margin: 0px auto; padding: 0px; }"
        ".line-dash { border-top: #ffffff dashed 1px; width: 60%; margin: 0px auto; padding: 1px; }")

vocabulary_model = genanki.Model(vocabulary_model_id, 'Vocabulary Model',
    fields=[
        {'name': 'Vocabulary'},
        {'name': 'Kana'},
        {'name': 'Meaning'},
        {'name': 'Level'},
        {'name': 'VocabID'},
    ],
    templates=[
        {
            'name': 'WaniAnki Vocabulary',
            'qfmt': '<div class="style-level">Level {{Level}}</div>'
                    '<div class="style-front">{{Vocabulary}}</div>',
            'afmt': '<div class="style-level">Level {{Level}}</div>'
                    '<img src="v{{VocabID}}.png">'
                    '<div class="line-dash"></div>'
                    '<p class="style-reading">{{Kana}}</p>'
                    '<p class="style-meaning">{{Meaning}}</p>'
        },
    ],
    css=".card { position: relative; text-align:center; color: #ffffff; background: #a100f1; margin: 0px auto; padding: 0px; }"
        ".style-front { font-size: 85px; margin: 0px auto; padding-top: 15px; }"
        ".style-meaning { font-size: 20px; margin: 0px auto; padding-top: 20px; }"
        ".style-level { font-size: 10px; font-weight: bold; position: absolute; top: 0; right: 0; margin: 0px; padding: 0px; }"
        ".style-reading { font-size: 25px; margin: 0px auto; padding-top: 25px; }"
        ".line-dash { border-top: #ffffff dashed 1px; width: 60%; margin: 0px auto; padding: 1px; }")

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
            'qfmt': '<div class="style-level">Level {{LevelR}}</div>'
                    '<div class="style-front">{{MeaningR}}</div>',
            'afmt': '<div class="style-level">Level {{LevelR}}</div>'
                    '<div class="style-front">{{MeaningR}}</div>'
                    '<div class="line-dash"></div>'
                    '<img src="v{{VocabIDR}}.png">'
                    '<p class="style-reading">{{KanaR}}</p>',
        },
    ],
    css=".card { position: relative; text-align:center; color: #ffffff; background: #a100f1; margin: 0px auto; padding: 0px; }"
        ".style-front { font-size: 50px; margin: 0px auto; padding: 20px 0px; }"
        ".style-level { font-size: 10px; font-weight: bold; position: absolute; top: 0; right: 0; margin: 0px; padding: 0px; }"
        ".style-reading { font-size: 25px; margin: 0px auto; padding: 5px 0px; }"
        ".line-dash { border-top: #ffffff dashed 1px; width: 60%; margin: 0px auto; padding-top: 10px; }")

wanikani_all = genanki.Deck(wanianki_kanji_and_vocab_id, 'WaniAnki Kanji & Vocabulary')
kanji_level = []
vocabulary = []
vocabulary_kana = []
vocabulary_meaning = []
vocabulary_level = []
vocabularyR = []
vocabulary_kanaR = []
vocabulary_meaningR = []
vocabulary_levelR = []

maxlength = 0
level_counter = 1

kanji_id = 1
vocab_id = 1
vocab_reverse_id = 1

while level_counter < 61:
    with open('wanikani_kanji.json') as kanji:
        font = ImageFont.truetype("KanjiStrokeOrders_v4.001.ttf", 150)
        k = json.load(kanji)
        sortlevel = [x for x in k['requested_information'] if 'level' in x]
        kanji_by_level = sorted(sortlevel, key=lambda x: x['level'])

        for kan in kanji_by_level:
            if kan['level'] == level_counter:
                kanji_character = kan['character']
                img = Image.new("RGB", (200, 200), (241, 0, 161))
                draw = ImageDraw.Draw(img)
                draw.text((20, 0), kanji_character, (255, 255, 255), font=font)
                draw = ImageDraw.Draw(img)
                img.save(str(kanji_id) + ".png")

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
                save_kanji_id = str(kanji_id)
                print('Building kanji card: ' + save_kanji_id + ', level ' + kanji_level + ': ' + kanji_character)
                if kanji_reading == 'onyomi':
                    new_note = genanki.Note(model=kanji_model, fields=[kanji_character, kanji_meaning, kanji_onyomi, kanji_kunyomi, kanji_nanori, kanji_onyomi, kanji_level, save_kanji_id])
                    wanikani_all.add_note(new_note)
                elif kanji_reading == 'kunyomi':
                    new_note = genanki.Note(model=kanji_model, fields=[kanji_character, kanji_meaning, kanji_onyomi, kanji_kunyomi, kanji_nanori, kanji_kunyomi, kanji_level, save_kanji_id])
                    wanikani_all.add_note(new_note)
                elif kanji_reading == 'nanori':
                    new_note = genanki.Note(model=kanji_model, fields=[kanji_character, kanji_meaning, kanji_onyomi, kanji_kunyomi, kanji_nanori, kanji_kunyomi, kanji_level, save_kanji_id])
                    wanikani_all.add_note(new_note)
                kanji_id += 1

    with open('wanikani_vocabulary.json') as vocab:
        font = ImageFont.truetype("KanjiStrokeOrders_v4.001.ttf", 100)
        v = json.load(vocab)
        sortlevel = [x for x in v['requested_information'] if 'level' in x]
        vocab_by_level = sorted(sortlevel, key=lambda x: x['level'])

        for voc in vocab_by_level:
            if voc['level'] == level_counter:
                vocabulary = voc['character']
                charlength = len(vocabulary)
                width = (charlength * 103) + (50 - (charlength * 5))
                img = Image.new("RGB", (width, 140), (161, 0, 241))
                draw = ImageDraw.Draw(img)
                draw.text((20, 0), vocabulary, (255, 255, 255), font=font)
                draw = ImageDraw.Draw(img)
                img.save('v' + str(vocab_id) + '.png')
                vocabulary_kana = voc['kana']
                vocabulary_meaning = voc['meaning']
                vocabulary_level = str(voc['level'])
                save_vocab_id = str(vocab_id)
                print('Building vocab card ' + save_vocab_id + ', level ' + vocabulary_level + ': ' + vocabulary)
                new_note = genanki.Note(model=vocabulary_model, fields=[vocabulary, vocabulary_kana, vocabulary_meaning, vocabulary_level, save_vocab_id])
                wanikani_all.add_note(new_note)
                vocab_id += 1

    with open('wanikani_vocabulary.json') as vocab:
        font = ImageFont.truetype("KanjiStrokeOrders_v4.001.ttf", 100)
        v = json.load(vocab)
        sortlevel = [x for x in v['requested_information'] if 'level' in x]
        vocab_by_level = sorted(sortlevel, key=lambda x: x['level'])

        for voc in vocab_by_level:
            if voc['level'] == level_counter:
                vocabularyR = voc['character']
                charlength = len(vocabularyR)
                width = (charlength * 103) + (50 - (charlength * 5))
                img = Image.new("RGB", (width, 140), (161, 0, 241))
                draw = ImageDraw.Draw(img)
                draw.text((20, 0), vocabularyR, (255, 255, 255), font=font)
                draw = ImageDraw.Draw(img)
                img.save('v' + str(vocab_reverse_id) + 'R.png')
                vocabulary_kanaR = voc['kana']
                vocabulary_meaningR = voc['meaning']
                vocabulary_levelR = str(voc['level'])
                save_vocab_reverse_id = str(vocab_reverse_id)
                print('Building reverse vocab card ' + save_vocab_reverse_id + ', level ' + vocabulary_levelR + ': ' + vocabularyR)
                new_note_reverse = genanki.Note(model=vocabulary_reverse_model, fields=[save_vocab_reverse_id, vocabularyR, vocabulary_kanaR, vocabulary_meaningR, vocabulary_levelR])
                wanikani_all.add_note(new_note_reverse)
                vocab_reverse_id += 1
    level_counter += 1

wanianki_media_files = []

kanji_id_range = range(1, kanji_id)
for i in kanji_id_range:
    wanianki_media_files.append(str(i) + '.png')

vid_rangeR = range(1, vocab_reverse_id)
for i in vid_rangeR:
    wanianki_media_files.append('v' + str(i) + 'R.png')

vid_range = range(1, vocab_id)
for i in vid_range:
    wanianki_media_files.append('v' + str(i) + '.png')

wanikani_all_package = genanki.Package(wanikani_all)
wanikani_all_package.media_files = wanianki_media_files
wanikani_all_package.write_to_file('wanikani_all.apkg')
