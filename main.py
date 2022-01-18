__author__ = "António Ramos"

"""
    References:
        - http://python.w3.pt/?p=234 -> portuguese stop words
        - https://www.geeksforgeeks.org/removing-stop-words-nltk-python/?fbclid=IwAR2zHEfPOxfInCRJ5QEdXc56worsVdNhdn7YB680jp3pU9Zf-La07FEhQac    
"""
from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
import time 
import nltk # install pip install nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
results_exact_file = "results_exact.csv"
results_ssc_file = "results_ssc_count.csv"
results_time = "results_time.csv"

def available_books():
    bible = "books/bible.txt"
    maias = "books/os_maias-eps_vida_romantica.txt"
    quijote = "books/don_quijote.txt"

    try:
        nltk.download('stopwords')
        nltk.download('punkt')
        stop_words_eng = set(nltk.corpus.stopwords.words('english'))
        stop_words_pt = set(nltk.corpus.stopwords.words('portuguese'))
        stop_words_sp = set(nltk.corpus.stopwords.words('spanish'))

        print("\n\nChoose a book between the followings \n")
        print(f"0 - {bible}")
        print(f"1 - {maias}")
        print(f"2 - {quijote}")

        choice = int(input())
        if choice == 0: 
            return bible, stop_words_eng
        if choice == 1:
            return maias, stop_words_pt
        if choice == 2:
            return quijote, stop_words_sp

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
    """ creating files with time results"""
    file = open(results_exact_file, "w")
    file.write("Word, Count, Time_exc\n")
    file.close()
    file_ssc_count = open(results_ssc_file, "w")
    file_ssc_count.write("Word, Count, Time_exc\n")
    file_ssc_count.close()
    file_time = open(results_time, "w")
    file_time.write("Exact_Count, SSC, K\n")
    file_time.close()


def write_results(exact_count, time_exc_count):
    """ write results of exact count in new file """
    file = open(results_exact_file, "a")
    exact_count = dict(sorted(exact_count.items(),key=lambda x:x[0],reverse = False))
    for word in exact_count:
        file.write(f"{word}, {exact_count[word]}, {time_exc_count}\n")
    file.close()


def write_results_ssc_count(ssc_count, time_ssc_count, k):
    """ write results of ssc_count and k in new file """
    file = open(results_ssc_file, "a")
    ssc_count = dict(sorted(ssc_count.items(),key=lambda x:x[0],reverse = False))
    for word in ssc_count:
        file.write(f"{word}, {ssc_count[word]}, {time_ssc_count}, {k}\n")
    file.close()


def write_time_analysis(exact_count, ssc_count):
    """ write time results """
    file = open(results_time, "a")
    for k in ssc_count:
        file.write(f"{exact_count},{ssc_count[k]}, {k}\n")
    file.close()


def write_image(exact_count, ssc_count):
    names = ['exact_count']
    values = [exact_count]
    
    for k in ssc_count:
        names.append(f"ssc_k_{k}")
        values.append(ssc_count[k])

    fig = plt.figure(figsize = (10, 5))
    plt.plot(names, values)
    plt.xlabel("Counter")
    plt.ylabel("Time")
    plt.title("Results time")
    plt.savefig("results_time")
    plt.close(fig)

def relative_error(exact_count, ssc_count):
    """ https://www.greelane.com/pt/ci%c3%aancia-tecnologia-matem%c3%a1tica/ci%c3%aancia/how-to-calculate-percent-error-609584/ """
    rel_error = {}
    rel_error_tmp = {}
    for k in ssc_count:
        if k not in rel_error:
            for word in ssc_count[k]:
                if word not in rel_error_tmp:
                    rel_error_tmp[word] = round(abs(exact_count[word]-ssc_count[k][word])/exact_count[word], 3)
            rel_error[k] = rel_error_tmp
    return rel_error          


if __name__ == "__main__":
    create_results_file()
    book, stopWords = available_books()
    book_name = book.split(".")
    book_name = book_name[0].split("/")
    words, exec_time_reading = read_file(book, stopWords)
    exact_count, exec_time_exact_count = exact_counts(words)
    print(f"Time of reading and processing the book {book} is {exec_time_reading} seconds\n")
    print(f"Time of Exact counter is {exec_time_exact_count} seconds\n")
    write_results(exact_count, exec_time_exact_count)
    list_k = [10, 25, 50, 70]
    times_ssc = {}
    ssc_count_dic = {}
    for k in list_k:
        if k > 5:
            ssc_count, exec_time_ssc = space_saving_count(words, k)
            print(f"Time of Space Saving Count is {exec_time_ssc} seconds with k = {k}")
            write_results_ssc_count(ssc_count, exec_time_ssc, k)
            if k not in times_ssc:
                times_ssc[k] = exec_time_ssc
            if k not in ssc_count_dic:
                ssc_count_dic[k] = ssc_count
    write_time_analysis(exec_time_exact_count, times_ssc)
    write_image(exec_time_exact_count, times_ssc)
    rel_error = relative_error(exact_count, ssc_count_dic)
    print(rel_error)