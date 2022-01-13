__author__ = "António Ramos"

"""
    References:
        - http://python.w3.pt/?p=234 -> portuguese stop words
        - https://www.geeksforgeeks.org/removing-stop-words-nltk-python/?fbclid=IwAR2zHEfPOxfInCRJ5QEdXc56worsVdNhdn7YB680jp3pU9Zf-La07FEhQac    
"""
import time 
import nltk # install pip install nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def available_books():
    bible = "books/bible.txt"
    maias = "books/os_maias-eps_vida_romantica.txt"
    quijote = "books/don_quijote.txt"
    test_eng = "books/test_english.txt"
    test_port = "books/test_port.txt"

    try:
        nltk.download('stopwords')
        nltk.download('punkt')
        stop_words_eng = set(nltk.corpus.stopwords.words('english'))
        stop_words_pt = set(nltk.corpus.stopwords.words('portuguese'))

        print("\n\nChoose a book between the followings \n")
        print(f"0 - {bible}")
        print(f"1 - {maias}")
        print(f"2 - {quijote}")
        print(f"3 - {test_eng}")
        print(f"4 - {test_port}")
        choice = int(input())
        if choice == 0: 
            return bible, stop_words_eng
        if choice == 1:
            return maias, stop_words_pt
        if choice == 2:
            return quijote
        if choice == 3:
            return test_eng, stop_words_eng
        if choice == 4:
            return test_port, stop_words_pt
    except ValueError:
        print("Please input integer only...")  


def read_file(book, stop_words):
    words = []
    file = open(book, "r", encoding='utf-8')
    start = time.time()

    for line in file:
        word_tokens = word_tokenize(line.lower()) # tokenize words

        for word in word_tokens:
            if word.isalpha() == True:
                if word not in stop_words:
                    words.append(word)

    stop = time.time() - start    
    file.close()
    return words, round(stop, 3)

# do exact coutings of words
def exact_counts(words):
    exact_count = {}
    start = time.time()
    for word in words:
        if word not in exact_count:
            exact_count[word] = 1
        else:
            exact_count[word] += 1
    stop = time.time() - start 
    return exact_count, round(stop, 3)


def space_saving_count(words, k):
    ssc_count = {}
    start = time.time()
    for word in words:
        if word not in ssc_count:
            if len(word) + 1 > k: 
                min_c = min(ssc_count, key=ssc_count.get)
                ssc_count[word] = ssc_count.pop(min_c) + 1
            else:
                ssc_count[word] = 1
        else:
            ssc_count[word] += 1
    stop = time.time() - start
    return ssc_count, round(stop, 3)

def create_results_file():
    file = open("results.csv", "w")
    file.write("Word, Exact_Count, Space_Saving_Count\n")
    file.close()

def write_results(words, exact_count, time_exc_count, ssc_count, time_ssc_count):
    file = open("results.csv", "a")
    for word in words:
        if word in exact_count and word in ssc_count:
            file.write(f"{word}, {exact_count[word]}, {time_exc_count}, {ssc_count[word]}, {time_ssc_count}\n")
    file.close()

if __name__ == "__main__":
    create_results_file()
    book, stopWords = available_books()
    words, exec_time_reading = read_file(book, stopWords)
    exact_count, exec_time_exact_count = exact_counts(words)
    print(f"Time of reading and processing the book {book} is {exec_time_reading} seconds\n")
    print(f"Time of Exact counter is {exec_time_exact_count} ")
    k = 5
    ssc_count, exec_time_ssc = space_saving_count(words, k)
    print(f"Time of Space Saving Count {exec_time_ssc}")
    write_results(words, exact_count, exec_time_exact_count, ssc_count, exec_time_ssc)
   

