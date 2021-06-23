from io import TextIOWrapper
import requests
import sys
from bs4 import BeautifulSoup

def print_words(wordlist, limit):
    print_text = ""
    for word in wordlist[:limit]:
        print_text +=word + "\n"
    return print_text

def print_examples(examplelist, limit):
    print_text = ""
    for i in range(0, limit * 2, 2):
        print_text += examplelist[i] + "\n"
        print_text += examplelist[i + 1] + "\n"
        print_text += "\n"
    return print_text

def get_userinput(langlist):
    print("Hello, you're welcome to the translator. Translator supports:")
    for i, lang in enumerate(langlist):
        print(f"{i}. {lang}") 

    print("Type the number of your language:")
    from_lang = langlist[int(input())]
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    to_lang = langlist[int(input())]
    print("Type the word you want to translate:")
    word = input().lower()

    return from_lang, to_lang, word

def translate(from_lang, to_lang, word, session, limit):
    print_text = ""
    url = f"https://context.reverso.net/translation/{from_lang.lower()}-{to_lang.lower()}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = session.get(url, headers=headers)
    if res.status_code == 200:
        pass
    else:
        if res.status_code == 404:
            print(f"Sorry, unable to find {word}")
        else:
            print("Something wrong with your internet connection")
        sys.exit()

    soup = BeautifulSoup(res.content, 'html.parser')
    a_tags = soup.find_all(name="a", attrs={"class": "translation"})
    wordlist = []
    for i, a in enumerate(a_tags):
        if i == 0:
            continue
        word = a.text.strip()
        wordlist.append(word)
    print_text += f"{to_lang} Translations:\n"
    print_text += print_words(wordlist, limit)
    print_text += "\n"

    div_tags = soup.find_all(name="div", attrs={"class": "ltr"})
    exsamplelist = []
    for div in div_tags:
        atrlist = div.get_attribute_list("class")
        if "src" not in atrlist and "trg" not in atrlist: 
            continue
        example = div.text.strip()
        exsamplelist.append(example)
    print_text += f"{to_lang} Examples:\n"
    print_text += print_examples(exsamplelist, limit)
    print_text += "\n"
    return print_text

def translate_all(langlist, from_lang, word, session):
    text = ""
    for to_lang in langlist:
        if to_lang in ("All", from_lang):
            continue
        text += translate(from_lang, to_lang, word, session, 1) 
    return text

def get_command(langlist):
    from_lang = sys.argv[1].lower().capitalize() 
    to_lang = sys.argv[2].lower().capitalize() 
    word = sys.argv[3].lower()
    if from_lang not in langlist:
        print(f"Sorry, the program doesn't support {sys.argv[1]}")
        sys.exit()
    if to_lang not in langlist:
        print(f"Sorry, the program doesn't support {sys.argv[2]}")
        sys.exit()

    return from_lang, to_lang, word

session = requests.Session()
langlist = ("All", "Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish")
from_lang, to_lang, word = get_command(langlist)

if to_lang == "All":
    text = translate_all(langlist, from_lang, word, session)
else:
    text = translate(from_lang, to_lang, word, session, 5)

print()
print(text)
with open(word + ".txt", "w", encoding="utf-8") as f:
    f.write(text)
