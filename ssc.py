__author__ = "António Ramos"

"""
    References:
        - http://python.w3.pt/?p=234 -> portuguese stop words
        - https://www.geeksforgeeks.org/removing-stop-words-nltk-python/?fbclid=IwAR2zHEfPOxfInCRJ5QEdXc56worsVdNhdn7YB680jp3pU9Zf-La07FEhQac    
"""

import more_itertools
import numpy as np
import matplotlib.pyplot as plt
import time 
import nltk # install pip install nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


results_exact_file = "results/results_exact.csv"
results_ssc_file = "results/results_ssc_count.csv"
results_time = "results/results_time.csv"
results_count = "results/results_count_word.csv"
results_rel_error = "results/results_rel_error.csv"

# choose book to process
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

# read and process file
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

# calculate space saving count according to pdf's
def space_saving_count(words, k):
    ssc_count = {}
    start = time.time()
    for word in words:
        if word not in ssc_count:
            if len(ssc_count) + 1 > k: 
                min_c = min(ssc_count, key=ssc_count.get)
                ssc_count[word] = ssc_count.pop(min_c) + 1
            else:
                ssc_count[word] = 1
        else:
            ssc_count[word] += 1
    stop = time.time() - start
    return ssc_count, round(stop, 3)

# creating files with time results
def create_results_file():
    file = open(results_exact_file, "w")
    file.write("Word, Count, Time_exc\n")
    file.close()
    file_ssc_count = open(results_ssc_file, "w")
    file_ssc_count.write("Word, Count, Time_exc\n")
    file_ssc_count.close()
    file_time = open(results_time, "w")
    file_time.write("Exact_Count, SSC, K\n")
    file_time.close()
    file_count = open(results_count, "w")
    file_count.write("Word, Exact_Count, SSC_Count, k\n")
    file_count.close()


# write results of exact count and the time of execution in new file
def write_results(exact_count, time_exc_count):
    file = open(results_exact_file, "a")
    exact_count = dict(sorted(exact_count.items(),key=lambda x:x[0],reverse = False))
    for word in exact_count:
        file.write(f"{word}, {exact_count[word]}, {time_exc_count}\n")
    file.close()

# write results of ssc_count and k and the time of execution in new file
def write_results_ssc_count(ssc_count, time_ssc_count, k):
    file = open(results_ssc_file, "a")
    ssc_count = dict(sorted(ssc_count.items(),key=lambda x:x[0],reverse = False))
    for word in ssc_count:
        file.write(f"{word}, {ssc_count[word]}, {time_ssc_count}, {k}\n")
    file.close()

# write time results
def write_time_analysis(exact_count, ssc_count):
    file = open(results_time, "a")
    for k in ssc_count:
        file.write(f"{exact_count},{ssc_count[k]}, {k}\n")
    file.close()

# saves a graph of time of executation of the counts
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
    plt.savefig("results/results_time")
    plt.close(fig)

# calculate the relative error of ssc_count
def relative_error(exact_count, ssc_count):
    """ https://www.greelane.com/pt/ci%c3%aancia-tecnologia-matem%c3%a1tica/ci%c3%aancia/how-to-calculate-percent-error-609584/ """
    rel_error = {}
    rel_error_tmp = {}
    for k in ssc_count:
        if k not in rel_error:
            for word in ssc_count[k]:
                if word not in rel_error_tmp:
                    rel_error_tmp[word] = round(abs(exact_count[word]-ssc_count[k][word])/exact_count[word], 3) * 100
            rel_error[k] = dict(sorted(rel_error_tmp.items(), key = lambda x:x[0]))
    return rel_error          

# sort the counts and select top 5 to write on file
def sort_words_counts(exact_count, ssc_count):
    exact_count_sort = dict(sorted(exact_count.items(), key = lambda x:x[1], reverse=True))
    # exact_count_sort = list(dict(sorted(exact_count.items(), key = lambda x:x[0])))[:5]
    ssc_count_sort = {}

    for k in ssc_count:
        if k not in ssc_count_sort:
            ssc_count_sort[k] = dict(sorted(ssc_count[k].items(), key = lambda x:x[1], reverse=True))
    
    file_count = open(results_count, "a")
    ex = more_itertools.take(5, exact_count_sort.items())
    
    file_count.write(f"{ex}\n")

    for k in ssc_count_sort:
        ssc = more_itertools.take(5, ssc_count_sort[k].items())
        file_count.write(f"{k}: {ssc}\n")
    file_count.close()

# write information about rel erro
def write_rel_error(rel_error):
    file_rel = open(results_rel_error, "w")
    file_rel.write("word,k,percentage_rel_error\n")

    for k in rel_error:
        for word in rel_error[k]:
            file_rel.write(f"{word}, {k}, {rel_error[k][word]}\n")
        
    file_rel.close()
   
def image_rel_error(rel_error):
    dir = "results_rel_error/"
    k_10_words = [word for k in rel_error for word in rel_error[k] if k == 10]
    k_10_values = [rel_error[k][word] for k in rel_error for word in rel_error[k] if k == 10]
    k_25_words = [word for k in rel_error for word in rel_error[k] if k == 25]
    k_25_values = [rel_error[k][word] for k in rel_error for word in rel_error[k] if k == 25]
    k_50_words = [word for k in rel_error for word in rel_error[k] if k == 50]
    k_50_values = [rel_error[k][word] for k in rel_error for word in rel_error[k] if k == 50]
    k_70_words = [word for k in rel_error for word in rel_error[k] if k == 70]
    k_70_values = [rel_error[k][word] for k in rel_error for word in rel_error[k] if k == 70]

    fig = plt.figure(figsize = (20, 5))
    plt.bar(k_10_words, k_10_values, color = "green")
    plt.ylabel("Percentage of Relative Error")
    plt.xlabel("Word")
    plt.title("K=10")
    plt.savefig(f"{dir}results_rel_error_10")
    plt.close(fig)

    fig_25 = plt.figure(figsize=(20,5))
    plt.bar(k_25_words, k_25_values, color = "blue")
    plt.ylabel("Percentage of Relative Error")
    plt.xlabel("Word")
    plt.title("K=25")
    plt.savefig(f"{dir}results_rel_error_25")
    plt.close(fig_25)

    fig_50 = plt.figure(figsize=(40,5))
    plt.bar(k_50_words, k_50_values, color = "red")
    plt.ylabel("Percentage of Relative Error")
    plt.xlabel("Word")
    plt.title("K=50")
    plt.savefig(f"{dir}results_rel_error_50")
    plt.close(fig_50)

    fig_70 = plt.figure(figsize=(50,5))
    plt.bar(k_70_words, k_70_values, color = "yellow")
    plt.ylabel("Percentage of Relative Error")
    plt.xlabel("Word")
    plt.title("K=70")
    plt.savefig(f"{dir}results_rel_error_70")
    plt.close(fig_70)


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
    # tests
    write_time_analysis(exec_time_exact_count, times_ssc)
    write_image(exec_time_exact_count, times_ssc)
    rel_error = relative_error(exact_count, ssc_count_dic)
    write_rel_error(rel_error)
    image_rel_error(rel_error)
    sort_words_counts(exact_count, ssc_count_dic)