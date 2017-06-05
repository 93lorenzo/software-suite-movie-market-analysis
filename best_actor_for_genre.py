import string
import json
from Tkinter import *

#root = Tk()

'''def fetch(ent1, ent2, root):
    global GENRE
    GENRE = str(ent1.get())
    global NUMBER_OF_ACTORS
    NUMBER_OF_ACTORS = int(ent2.get())
    root.destroy()

def initialization():

    root.title("Best actor for genre")
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

class BestActor:

    def find_max(self,d):
        max = 0
        result = ""
        for actor in d.keys():
            score = d.get(actor)
            if score > max:
                max = score
                result = actor
        return result

    def main(self,GENRE,NUMBER_OF_ACTORS):
        file = open("invertedIndexActorsAll.txt", "r")
        actors = json.loads(file.readline())
        file.close()
        file = open("moviesAll.txt", "r")
        movies = json.loads(file.readline())
        file.close()
        d = {}

        for actor in actors:
            score = 0
            list_of_films = actors.get(actor)
            for id in list_of_films:
                movie = movies.get(id)
                if movie == None:
                    continue
                genres = movie.get("genre")
                for genre in genres:
                    if genre == "N/A":
                        continue
                    if genre == GENRE:
                        if actor not in d:
                            d[actor] = 0
                        rating = movie.get("imdbRating")
                        votes = movie.get("imdbVotes").replace(",","")
                        if votes == "N/A" or rating == "N/A":
                            continue
                        d[actor] += float(rating)*float(votes)
        results = []

        for _ in range(NUMBER_OF_ACTORS):
            result = self.find_max(d)
            results.append(result)
            d[result] = 0
        return results
        #self.print_result(results, GENRE, NUMBER_OF_ACTORS)

        #for elem in results:
            #print "actor : " + elem