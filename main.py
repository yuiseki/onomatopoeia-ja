import datasets

# onomatopoeia_list
# onomatopoeia_ja: onomatopoeia in Japanese
# translate_en: onomatopoeia in English
# detains_en: details in English
# details_ja: details in Japanese
onomatopoeia_list = []

jp_onomatopoeia = datasets.load_dataset("json", data_files = "tmp/nsk.sh/tools/jp-onomatopoeia/onomatopoeia.jsonnl")
for i in range(len(jp_onomatopoeia['train'])):
    onomatopoeia = jp_onomatopoeia['train'][i]
    onomatopoeia_ja = onomatopoeia['key']
    translate_en = []
    details_en = []
    details_ja = []
    for value in onomatopoeia['value']:
        if "english" in value:
            en = value['english'].replace("\"", "")
            en = en.replace("*", "")
            en = en.split(", ")
            translate_en = translate_en + en
        if "details" in value and value['details'] is not None:
            details_en.append(value['details'])
    new_onomatopoeia = {
        "onomatopoeia_ja": onomatopoeia_ja,
        "translate_en": translate_en,
        "details_ja": details_ja,
        "details_en": details_en
    }
    onomatopoeia_list.append(new_onomatopoeia)

giongo = datasets.load_dataset("csv", data_files = "tmp/Pomax/nihongoresources.com/giongo.txt", delimiter='\t')
for i in range(len(giongo['train'])):
    onomatopoeia = giongo['train'][i]
    onomatopoeia_ja = onomatopoeia['hiragana']
    translate_en = []
    details_en = []
    if "translation" in onomatopoeia:
        en = onomatopoeia['translation'].replace("\"", "").split(", ")
        translate_en = translate_en + en
    if "applies to" in onomatopoeia:
        details_en = ["applies to " + onomatopoeia['applies to']]
    details_ja = []
    new_onomatopoeia = {
        "onomatopoeia_ja": onomatopoeia_ja,
        "translate_en": translate_en,
        "details_ja": details_ja,
        "details_en": details_en
    }
    # check if the onomatopoeia is already in the list
    if onomatopoeia_ja not in [x['onomatopoeia_ja'] for x in onomatopoeia_list]:
        onomatopoeia_list.append(new_onomatopoeia)
    else:
        # merge values
        index = [x['onomatopoeia_ja'] for x in onomatopoeia_list].index(onomatopoeia_ja)
        onomatopoeia_list[index]['translate_en'] = list(set(onomatopoeia_list[index]['translate_en'] + translate_en))
        onomatopoeia_list[index]['details_en'] = list(set(onomatopoeia_list[index]['details_en'] + details_en))
        onomatopoeia_list[index]['details_ja'] = list(set(onomatopoeia_list[index]['details_ja'] + details_ja))

surasura = datasets.load_dataset("json", data_files = "tmp/surasura/term_bank_1.jsonnl")
for i in range(len(surasura['train'])):
    onomatopoeia = surasura['train'][i]
    onomatopoeia_ja = onomatopoeia['key']
    translate_en = []
    details_en = []
    details_ja = []
    if "value" in onomatopoeia:
        for content in onomatopoeia['value']:
            if "content" in content:
                details_ja.append(content['content'])
    new_onomatopoeia = {
        "onomatopoeia_ja": onomatopoeia_ja,
        "translate_en": translate_en,
        "details_ja": details_ja,
        "details_en": details_en
    }
    # check if the onomatopoeia is already in the list
    if onomatopoeia_ja not in [x['onomatopoeia_ja'] for x in onomatopoeia_list]:
        onomatopoeia_list.append(new_onomatopoeia)
    else:
        # merge values
        index = [x['onomatopoeia_ja'] for x in onomatopoeia_list].index(onomatopoeia_ja)
        onomatopoeia_list[index]['translate_en'] = list(set(onomatopoeia_list[index]['translate_en'] + translate_en))
        onomatopoeia_list[index]['details_en'] = list(set(onomatopoeia_list[index]['details_en'] + details_en))
        onomatopoeia_list[index]['details_ja'] = list(set(onomatopoeia_list[index]['details_ja'] + details_ja))

# convert to dataset
onomatopoeia_dataset = datasets.Dataset.from_list(onomatopoeia_list)

# print(onomatopoeia_dataset)

# onomatopoeia_dataset.push_to_hub("yuiseki/onomatopoeia-ja")

text_to_onomatopoeia_list = []
for i in range(len(onomatopoeia_list)):
    onomatopoeia = onomatopoeia_list[i]
    onomatopoeia_ja = onomatopoeia['onomatopoeia_ja']
    if not "details_ja" in onomatopoeia:
        continue
    for detail in onomatopoeia['details_ja']:
        new_onomatopoeia = {
            "text": detail,
            "text_lang": "ja",
            "onomatopoeia_ja": onomatopoeia_ja,
        }
        text_to_onomatopoeia_list.append(new_onomatopoeia)
    if not "details_en" in onomatopoeia:
        continue
    for detail in onomatopoeia['details_en']:
        if detail == "manga sound effects":
            continue
        new_onomatopoeia = {
            "text": detail,
            "text_lang": "en",
            "onomatopoeia_ja": onomatopoeia_ja,
        }
        text_to_onomatopoeia_list.append(new_onomatopoeia)



text_to_onomatopoeia_dataset = datasets.Dataset.from_list(text_to_onomatopoeia_list)
text_to_onomatopoeia_dataset.push_to_hub("yuiseki/onomatopoeia-ja-flat")
