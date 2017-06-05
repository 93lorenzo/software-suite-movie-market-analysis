import json
import string
from Tkinter import *


'''def fetch(ent1, ent2, root):
    global GENRE
    GENRE = str(ent1.get())
    global NUMBER_OF_RESULTS
    NUMBER_OF_RESULTS = int(ent2.get())
    root.destroy()

def initialization():

    root.title("Most popular movies by genre")
    Label(root, text=" Please type genre and number of results you want to display: ").pack()

    row1 = Frame(root)
    title1 = Label(row1, text="Genre", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    ent1 = Entry(row1)
    #var1 = StringVar(row1)
    ent1.pack(side =RIGHT)
    row1.pack(side=TOP, fill=X, padx=5, pady=5)

    row2 = Frame(root)
    title2 = Label(row2, text="Number of results", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    ent2 = Entry(row2)
    #var2 = StringVar(row2)
    ent2.pack(side=RIGHT)
    row2.pack(side=TOP, fill=X, padx=5, pady=5)

    ents = ""
    root.bind('<Return>', (lambda event, e = ents: fetch(ent1, ent2, root)))

    # this button calls the method passed
    b1 = Button(root, text='Show', command=(lambda e = ents: fetch(ent1, ent2, root)))
    b1.pack(side=LEFT, padx=10, pady=10)

    # this button quits the app
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=RIGHT, padx=10, pady=10)

    row1.pack(pady = 10)
    row2.pack(pady = 10)

    root.wm_minsize(width= 120,height= 120)
    root.mainloop()'''


'''def print_result(self,result, GENRE, NUMBER_OF_RESULTS):
    root = Tk()
    root.title("Most popular movies by genre")
    string1 = "The " + str(NUMBER_OF_RESULTS) + " most famous " + GENRE.lower() + " movies are printed"
    string2 = "\non a file named \"result" + GENRE + str(NUMBER_OF_RESULTS) + ".txt\""
    label = Label(root, text = string1 + string2, font = ("Sans Serif" , 12 ,"bold"))
    label.pack(padx= 50, pady= 50)

    file = open("result" + GENRE + str(NUMBER_OF_RESULTS) + ".txt", "w")
    for elem in result:
        atif = movies.get(elem[0])
        file.write(atif.get("title").encode("utf-8") + "\n")

    b2 = Button(root, text='Ok', command=root.quit)
    b2.pack(padx=20, pady=20)

    root.wm_minsize(width=120, height=120)
    root.mainloop()'''

class MostPopularGenre:
    def put_in_scores(self,movie, scores):
        min = 4294967295
        for elem in scores:
            if elem[1] < min:
                min = elem[1]
        if movie[1] > min:
            for i in range(len(scores)):
                if min == scores[i][1]:
                    scores[i] = movie
                    break

        return scores

    def find_max(self,result):
        max = 0
        tuple = []
        index = 0
        i = -1
        for elem in result:
            i += 1
            if elem[1] > max:
                max = elem[1]
                tuple = elem
                index = i
        return tuple, index

    def sort_tuples(self,result):
        list = []
        size = len(result)
        for _ in range(size):
            tuple, index = self.find_max(result)
            list.append(tuple)
            result[index][1] = 0
        return list

    def main(self,GENRE,NUMBER_OF_RESULTS):
        file1 = open("moviesAll.txt", "r")
        #file2 = open("moviesTest10-1970.txt", "r")
        movies = json.loads(file1.readline())
        #movies1970 = json.loads(file2.readline())
        file1.close()
        #file2.close()

        d = {}
        for id in movies:
            movie = movies.get(id)
            genres = movie.get("genre")
            rating = movie.get("imdbRating")
            votes = movie.get("imdbVotes").replace(",","")
            if votes == "N/A" or rating == "N/A" or genres == "N/A":
                continue
            for genre in genres:
                if genre in d:
                    d[genre].append([id, float(rating)*float(votes)])
                else:
                    d[genre] = []
                    d[genre].append([id, float(rating)*float(votes)])

        '''for id in movies1970:
            movie = movies1970.get(id)
            genres = movie.get("genre")
            rating = movie.get("imdbRating")
            votes = movie.get("imdbVotes").translate(None, string.punctuation)
            if votes == "N/A" or rating == "N/A" or genres == "N/A":
                continue
            for genre in genres:
                if genre in d:
                    d[genre].append([id, float(rating)*float(votes)])
                else:
                    d[genre] = []
                    d[genre].append([id, float(rating)*float(votes)])'''

        drama = d.get(GENRE)
        result = []
        for i in range (NUMBER_OF_RESULTS):
            result.append(["", 0])
        for elem in drama:
            self.put_in_scores(elem, result)

        result = self.sort_tuples(result)
        #print_result(result, GENRE, NUMBER_OF_RESULTS)
        results = []
        for elem in result:
            results.append(movies.get(elem[0]).get("title"))
        return results
