from Tkinter import *
import tkFileDialog as fd
from tkFont import Font
import json
import numpy as np
import testMovies as TM
import best_actor_for_genre as BA
import most_popular_by_genre as MPG

fields = 'Actor', 'Director', 'Writer','Rating'
ACTOR_NUMBER = 4
WRITER_NUMBER = 2
DIRECTOR_NUMBER = 2
RATING_NUMBER = 1

fileResult = "Results.csv"

#file = open("moviesTest-1970.txt",'r')
act = open("invertedIndexActorsWeightedAll.txt",'r')
dir = open("invertedIndexDirectorsWeightedAll.txt", 'r')
wri = open("invertedIndexWritersWeightedAll.txt", 'r')
#line = file.readline()
lact = act.readline()
ldir = dir.readline()
lwri = wri.readline()
#gson = json.loads(line)
jact = json.loads(lact)
jdir = json.loads(ldir)
jwri = json.loads(lwri)
#file.close()
act.close()
dir.close()
wri.close()
my_list =  [[] for x in xrange(0,4)]

genres = ["Sci-Fi","Crime","Romance","Animation","Music/Musical","Comedy","War","Horror","Adventure","Thriller",
          "Western","Mystery","Short","Drama","Action","Documentary","History","Family","Fantasy","Sport","Biography"]
genres = np.sort(genres)

nums = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
k = 0
for elem in jact:
    if float((jact).get(elem).get("rating")) < 6.5:
        continue
    else:
        my_list[0].append(elem)
for elem in jdir:
    my_list[1].append(elem)
for elem in jwri:
    if float((jwri).get(elem).get("rating")) < 5:
        continue
    else:
        my_list[2].append(elem)
    #my_list[2].append(elem)
my_list[3] = [1,2,3,4,5]

my_list[0]= np.sort(my_list[0])
my_list[1]= np.sort(my_list[1])
my_list[2]= np.sort(my_list[2])



ACTOR_FLAG = 0

# actor list 

init = Tk()


def fetchPredSingle(entries,titleE,root):
    res = Tk()
    titolo = titleE.get()
    #print('%s: "%s"' % ("Title", titolo))
    fields = []
    for entry in entries:
        fields.append(entry[1].get())
        #print('%s: "%s"' % (field, text))
    #root.quit()
    root.destroy()
    t = TM.Test()
    label = t.init(fields[0:ACTOR_NUMBER],fields[ACTOR_NUMBER:ACTOR_NUMBER+DIRECTOR_NUMBER]
                   ,fields[ACTOR_NUMBER+DIRECTOR_NUMBER:ACTOR_NUMBER+DIRECTOR_NUMBER+WRITER_NUMBER])

    s = "THE PREDICTED RATING IS: "+str(label)
    Label(res,text = s,font = ("Sans Serif" ,12 ,"bold" )).pack(padx = 20,pady=20)
    b = Button(res, text='Close', command=res.quit)
    b.pack(padx=10, pady=10)


def fetchPredSet(filename,root):
   t = TM.Test()
   correct = t.init2(filename,fileResult)
   s1 = "Done"
   #s1 =  "ACCURACY ON TEST FILE IS: " + str(correctness) + "% "
   s2 = " YOU CAN FIND THE RESULT ON "+str(fileResult).upper()
   result = Tk()
   Label(result,text = s1,font = ("Sans Serif" ,12 ,"bold" )).pack(padx = 20,pady=20)

   Label(result, text = s2, font=("Sans Serif", 12, "bold")).pack()
   b2 = Button(result, text='Close', command=root.quit)
   b2.pack(side=BOTTOM, padx=10, pady=10)
   root.destroy()



def fill_form(root,field,entries,id_list):
   row = Frame(root)
   lab = Label(row, width=15, text=field, font = ("Sans Serif" ,12 ,"bold" ) , anchor='w')
   ent = Entry(row)

   var = StringVar(row)
   var.set("None")

   drop_menu = OptionMenu(row, var, *my_list[id_list], command=grab_and_assign)
   drop_menu.pack(side=RIGHT,fill=X)


   row.pack(side=TOP, fill=X, padx=5, pady=5)
   lab.pack(side=LEFT)
   
   entries.append((field, var))
   #entries.append((field, ent))


def fill_form_best_actors_most_popular(root,field,entries,lista):
    row = Frame(root)
    lab = Label(row, width=15, text=field, font=("Sans Serif", 12, "bold"), anchor='w')
    ent = Entry(row)

    var = StringVar(row)
    var.set("None")

    drop_menu = OptionMenu(row, var, *lista, command=grab_and_assign)
    drop_menu.pack(side=RIGHT, fill=X)

    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)

    entries.append((field, var))

def grab_and_assign(var):
   print "current changed "


def makeform(root, fields):
   entries = []
   # loop to fill all the fields
   for field in fields:
      
      if field == "Actor" : 
         for i in range( ACTOR_NUMBER ) :
            fill_form(root,field+" "+str(i+1),entries,0)
      
      if field == "Director" : 
         for i in range( DIRECTOR_NUMBER ) :
            fill_form(root,field+" "+str(i+1),entries,1)
      
      if field == "Writer" : 
         for i in range( WRITER_NUMBER ) :
            fill_form(root,field+" "+str(i+1),entries,2)

   return entries


def makeformBestActorsMostPopular(root, fields):
    entries = []
    # loop to fill all the fields
    for field in fields:
        if field == "Genre":
            fill_form_best_actors_most_popular(root, field + " ", entries,genres)
        if field == "Number of actors":
            fill_form_best_actors_most_popular(root, field + " ", entries,nums)
    return entries



def initialization():

    init.title("Welcome to S.S.M.M.A.")
    #init.bind('<Return>', (lambda event: main()))
    Label(init, text=" Please choose the option that you prefer: ").pack()
    row1 = Frame(init)
    title = Label(row1, text=" Rating prediction for a single movie ", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    b1 = Button(row1, text= "Open", command = lambda :mainPredSingle(init))
    b1.pack(side = RIGHT)
    row2 = Frame(init)
    title = Label(row2, text=" Rating Prediction for a set of movies ", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    b2 = Button(row2, text="Open", command = lambda :mainPredSet(init))
    b2.pack(side = RIGHT)
    row3 = Frame(init)
    title = Label(row3, text=" Best actors ranking for genre ", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    b3 = Button(row3, text="Open", command=lambda: bestActor(init))
    b3.pack(side=RIGHT)
    row4 = Frame(init)
    title = Label(row4, text=" Most popular movies for genre ", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    b4 = Button(row4, text="Open", command=lambda: mostPopularGenre(init))
    b4.pack(side=RIGHT)
    row1.pack(pady = 10)
    row2.pack(pady = 10)
    row3.pack(pady=10)
    row4.pack(pady=10)
    init.wm_minsize(width= 120,height= 120)
    init.mainloop()


def print_result(tk,result, GENRE, NUMBER,ACTOR_FLAG):
    tk.destroy()
    root = Tk()
    if(ACTOR_FLAG):
        root.title("Best actor for genre")
        string1 = "The " + str(NUMBER) + " most famous " + GENRE.lower() + " actors are printed"
        string2 = "\non a file named \"actors" + GENRE + str(NUMBER) + ".txt\""
        label = Label(root, text=string1 + string2, font=("Sans Serif", 12, "bold"))
        label.pack(padx=50, pady=50)

        file = open("actors" + GENRE + str(NUMBER) + ".txt", "w")
    else:
        root.title("Most popular movies by genre")
        string1 = "The " + str(NUMBER) + " most famous " + GENRE.lower() + " movies are printed"
        string2 = "\non a file named \"result" + GENRE + str(NUMBER) + ".txt\""
        label = Label(root, text=string1 + string2, font=("Sans Serif", 12, "bold"))
        label.pack(padx=50, pady=50)

        file = open("result" + GENRE + str(NUMBER) + ".txt", "w")
    for elem in result:
        print elem
        file.write(elem.encode("utf-8") + "\n")

    b2 = Button(root, text='Ok', command=root.quit)
    b2.pack(padx=20, pady=20)

    root.wm_minsize(width=120, height=120)
    #root.mainloop()


def fetchBestActor(entries, root,ACTOR_FLAG):
    GENRE = str(entries[0][1].get())
    NUMBER = int(entries[1][1].get())
    if(ACTOR_FLAG):
        BACT =BA.BestActor()
        results = BACT.main(GENRE,NUMBER)
        print_result(root,results,GENRE,NUMBER,ACTOR_FLAG)
    else:
        MOSTPG = MPG.MostPopularGenre()
        results = MOSTPG.main(GENRE,NUMBER)
        print_result(root, results, GENRE, NUMBER,ACTOR_FLAG)


def mostPopularGenre(init):
    init.destroy()
    root = Tk()
    root.title("Most popular movies by genre")
    Label(root, text=" Please type genre and number of results you want to display: ").pack()

    '''row1 = Frame(root)
    title1 = Label(row1, text="Genre", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    ent1 = Entry(row1)
    # var1 = StringVar(row1)
    ent1.pack(side=RIGHT)
    row1.pack(side=TOP, fill=X, padx=5, pady=5)

    row2 = Frame(root)
    title2 = Label(row2, text="Number of results", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    ent2 = Entry(row2)
    # var2 = StringVar(row2)
    ent2.pack(side=RIGHT)
    row2.pack(side=TOP, fill=X, padx=5, pady=5)'''
    entries = makeformBestActorsMostPopular(root, ["Genre", "Number of actors"])
    ents = ""
    root.bind('<Return>', (lambda event, e=ents: fetchBestActor(entries, root, ACTOR_FLAG=0)))

    # this button calls the method passed
    b1 = Button(root, text='Show', command=(lambda e=ents: fetchBestActor(entries, root, ACTOR_FLAG=0)))
    b1.pack(side=LEFT, padx=10, pady=10)

    # this button quits the app
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=RIGHT, padx=10, pady=10)

    #row1.pack(pady=10)
    #row2.pack(pady=10)
    root.wm_minsize(width=120, height=120)

def bestActor(init):
    init.destroy()
    root = Tk()
    root.title("Best actor for genre")
    Label(root, text=" Please type genre and number of results you want to display: ").pack()
    entries = makeformBestActorsMostPopular(root,["Genre","Number of actors"])
    #ent1 = fill_form_Best_Actors(root,"genre")
    #row1 = Frame(root)
    #title1 = Label(row1, text="Genre", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    #ent1 = Entry(row1)
    # var1 = StringVar(row1)
    #ent1.pack(side=RIGHT)
    #row1.pack(side=TOP, fill=X, padx=5, pady=5)

    #row2 = Frame(root)
    #title2 = Label(row2, text="Number of results", font=("Sans Serif", 12, "bold")).pack(side=LEFT)
    #ent2 = Entry(row2)
    # var2 = StringVar(row2)
    #ent2.pack(side=RIGHT)
    #row2.pack(side=TOP, fill=X, padx=5, pady=5)

    ents = ""
    root.bind('<Return>', (lambda event, e=ents: fetchBestActor(entries, root,ACTOR_FLAG=1)))
    # this button calls the method passed
    b1 = Button(root, text='Show', command=(lambda e=ents: fetchBestActor(entries, root,ACTOR_FLAG=1)))
    b1.pack(side=LEFT, padx=10, pady=10)

    # this button quits the app
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=RIGHT, padx=10, pady=10)

    #row1.pack(pady=10)
    #row2.pack(pady=10)

    root.wm_minsize(width=120, height=120)
    #root.mainloop()



def mainPredSet(init):
    filename = fd.askopenfilename()
    root  = Tk()
    init.destroy()
    Label(root,text = " Testing data from file... ").pack(padx= 20,pady=20)
    root.wm_minsize(width=150, height=150)
    fetchPredSet(filename,root)





def mainPredSingle(init):
   # here there are the strings for the initial status
   root  = Tk()
   init.destroy()
   root.title("WELCOME TO THE FETA PROJECT")
   ss1 = " Welcome to the success movie predictor \n Leave empty the entries you don't need "
   ss2 = "\nand press the button to make the prediction"
   string = ss1+ss2
   Label(root, text=string,font = ("Sans Serif" ,12 ,"bold")).pack()

   row = Frame(root)
   title = Label(row, text = "Title",font = ("Sans Serif" ,12 ,"bold" )).pack(side = LEFT)
   titleE = Entry(row)
   titleE.pack(side = RIGHT)
   row.pack(side=TOP, fill=X, padx=5, pady=5)

   # Making the form
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetchPredSingle(e,titleE,root)))

   # this button calls the method passed
   b1 = Button(root, text='Show', command=(lambda e=ents: fetchPredSingle(e,titleE,root)))
   b1.pack(side=LEFT, padx=10, pady=10)

   # this button quits the app
   b2 = Button(root, text='Quit', command=root.quit)
   b2.pack(side=RIGHT, padx=10, pady=10)

   #root.mainloop()


#main()
initialization()





