# importing libraries
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import bs4 as BeautifulSoup
import urllib.request
import stopwordsiso as stopwords
from langdetect import detect


def average(sentence_weight) -> float:
    weight_sum = 0
    for i in sentence_weight:
        weight_sum += sentence_weight[i]

    return weight_sum / len(sentence_weight)


def get_article_summary(sentences, sentence_weight, avr):
    article_summary = ''
    sentence_number = 0

    for sentence in sentences:
        sentence_number += 1
        if sentence_number in sentence_weight \
                and sentence_weight[sentence_number] >= avr:
            article_summary += " " + sentence

    return article_summary


def calculate_sentence_weight(sentences, frequency_table) -> {}:
    sentence_weight = {}

    sentence_number = 0
    for sentence in sentences:
        stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                stop_words += 1
                sentence_number += 1
                if sentence_number in sentence_weight:
                    sentence_weight[sentence_number] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence_number] = frequency_table[word_weight]

        sentence_weight[sentence_number] = sentence_weight[sentence_number] / stop_words

    return sentence_weight


def create_frequency_table(text_string) -> {}:
    lang = detect(text_string)
    stop_words = stopwords.stopwords(lang)

    words = word_tokenize(text_string)
    stem = PorterStemmer()

    frequency_table = {}
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def summarizing(text_to_summer):
    frequency_table = create_frequency_table(text_to_summer)
    sentences = sent_tokenize(text_to_summer)
    sentence_scores = calculate_sentence_weight(sentences, frequency_table)
    avr = average(sentence_scores)
    summarized = get_article_summary(sentences, sentence_scores, avr)

    return summarized


def load_http(http_path):
    fetched_data = urllib.request.urlopen(http_path)

    article_read = fetched_data.read()

    article_parsed = BeautifulSoup.BeautifulSoup(article_read, 'html.parser')

    paragraphs = article_parsed.find_all('p')

    http = ''

    for p in paragraphs:
        http += p.text

    return http


def load_file(file_path):
    f = open(file_path, encoding='utf-8', mode="r")
    return f.read()


if __name__ == '__main__':
    print("Enter path to the text: ")
    path = input()
    text = ''
    if path.startswith("http"):
        text = load_http(path)
    else:
        text = load_file(path)

    if text != "":
        summary = summarizing(text)
        print(summary)
    else:
        print("No text found")
