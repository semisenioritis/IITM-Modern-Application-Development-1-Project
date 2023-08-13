from classes import Venue, Movie, Screening
import sqlite3
from fuzzywuzzy import fuzz
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import difflib
from fuzzywuzzy import process

def venue_creator(vnam,cap,rat,add,picblob,desc,ext):
    currvenue = Venue(vnam,cap,rat,add,picblob,desc)
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)

    conn.execute('''CREATE TABLE IF NOT EXISTS venue
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vname TEXT NOT NULL UNIQUE,
                    capacity INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    address TEXT NOT NULL,
                    photo BLOB NOT NULL,
                    description TEXT NOT NULL,
                    extt TEXT NOT NULL);''')

    cursor = conn.cursor()
    data = (currvenue.name, currvenue.capacity, currvenue.rating, currvenue.address, currvenue.photo, currvenue.description, ext)
    try:
        cursor.execute('INSERT INTO venue (vname, capacity, rating, address, photo, description, extt) VALUES (?, ?, ?, ?, ?, ?, ?)', data)
        # todo: DONE modify all functions that have something to do with venue to accomodate for the adding of two rows.
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def movie_creator(mname,genre,rat,tags,lang, price, picblob, desc, ext):
    currmovie= Movie(mname,genre,rat,tags,lang,price)
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)

    conn.execute('''CREATE TABLE IF NOT EXISTS movie
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mname TEXT NOT NULL UNIQUE,
                    genre TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    tags TEXT NOT NULL,  
                    lang TEXT NOT NULL,                  
                    price INTEGER NOT NULL,
                    photo BLOB NOT NULL,
                    description TEXT NOT NULL,
                    extt TEXT NOT NULL);''')

    cursor = conn.cursor()
    data = (currmovie.name, currmovie.genre, currmovie.rating, currmovie.tags, currmovie.languages, currmovie.price, picblob, desc, ext)
    try:
        cursor.execute('INSERT INTO movie (mname, genre, rating, tags, lang, price, photo, description, extt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
        # print("i just sucessfully pushed a movie into the db")
        return True
    except:
        conn.close()
        # print("movie pushing didnt work")
        return False


def ven_mov_finder():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    ven_list=[]
    mov_list=[]
    try:
        cursor.execute("SELECT vname FROM venue")
        ven_list = cursor.fetchall()
        conn.close()
    except:
        conn.close()
        pass

    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT mname FROM movie")
        mov_list = cursor.fetchall()
        conn.close()
    except:
        conn.close()
        pass
    return (ven_list, mov_list)

def show_creator(mname,vnam,date,time):

    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT capacity FROM venue WHERE vname=?",(vnam,))
        cap_list = cursor.fetchall()
        # print(vnam)
        # print(cap_list)
        # print(cap_list[0][0])
        cap_list = cap_list[0][0]
        # print("hi", cap_list)
        conn.close()
    except:
        cap_list=[]
        # print("no", cap_list)
        pass



    currshow= Screening(vnam,mname,date,time,cap_list)
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)


    conn.execute('''CREATE TABLE IF NOT EXISTS show
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mname TEXT NOT NULL ,
                    vname TEXT NOT NULL,
                    datee TEXT NOT NULL,
                    timee TEXT NOT NULL,
                    rem_seat INTEGER NOT NULL);''')

    cursor = conn.cursor()
    # print(currshow.number_of_seats_left)
    data = (currshow.movie, currshow.venue, currshow.date, currshow.time, int(currshow.number_of_seats_left))
    # print("i have created the data string")
    try:
        cursor.execute('INSERT INTO show (mname, vname, datee, timee, rem_seat) VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
        # print("i just sucessfully pushed a show into the db")
        return True
    except:
        conn.close()
        # print("show pushing didnt work")
        return False

def show_finder():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT vname FROM show")
        show_place_list = cursor.fetchall()
        # print(show_place_list)
        # print(show_place_list_fin)
        super_show_list=[]
        for i in show_place_list:
            cursor.execute("SELECT * FROM show WHERE vname=? ",i)
            listofshowsinvenue=cursor.fetchall()
            # print(listofshowsinvenue)
            super_show_list.append(listofshowsinvenue)
        conn.close()
    except:
        super_show_list=[]
        conn.close()

    return (super_show_list)



def ven_all_deets():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM venue")
        ven_list = cursor.fetchall()
        conn.close()
    except:
        ven_list=[]
        conn.close()
    return (ven_list)


def mov_all_deets():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM movie")
        mov_list = cursor.fetchall()
        conn.close()
    except:
        mov_list=[]
        conn.close()
        pass
    return (mov_list)

def show_all_deets():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM show")
        show_list = cursor.fetchall()
        conn.close()
    except:
        show_list=[]
        conn.close()
        pass
    return (show_list)

def editventable(newven,newcap,newrat,newadd,newpicblob,newdesc,newext,venindx,oldname):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    # print('atleast this works')
    try:
        if oldname != newven:
            inndata=(newven,oldname)
            try:
                innsql="UPDATE show SET vname =? WHERE vname=?"
                cursor.execute(innsql,inndata)
            except:
                pass
            # print("vennname changed and the cascade thingie worked")
        data=(newven,newcap,newrat,newadd,newpicblob,newdesc,newext,venindx)
        sql="UPDATE venue SET vname =?, capacity=?, rating=?, address=?, photo=?, description=?, extt=? WHERE id=?"
        # print("a satisfactory update to the venue table")
        cursor.execute(sql,data)
        conn.commit()
        conn.close()
    except:
        conn.close()
        pass


def editventablenopic(newven,newcap,newrat,newadd,newdesc,venindx,oldname):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    # print('atleast this works')
    # print(venindx)
    try:
        if oldname != newven:
            inndata=(newven,oldname)
            try:
                innsql="UPDATE show SET vname =? WHERE vname=?"
                cursor.execute(innsql,inndata)
            except:
                pass
            # print("vennname changed and the cascade thingie worked")
        data=(newven,newcap,newrat,newadd,newdesc,venindx)
        sql="UPDATE venue SET vname =?, capacity=?, rating=?, address=?, description=? WHERE id=?"

        cursor.execute(sql,data)
        # print("a satisfactory update to the venue table")
        conn.commit()
        # print("this worksSSSSSSSSSSSSSSS")
        conn.close()
    except:
        conn.close()
        pass

def editmovtable(newmov,newgenre,newrating,newtags,newlang,newprice,newpicblob,newdesc,newext,movindx,oldname):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        if oldname != newmov:
            inndata=(newmov,oldname)
            try:
                innsql="UPDATE show SET mname =? WHERE mname=?"
                cursor.execute(innsql,inndata)
            except:
                pass
        data=(newmov,newgenre,newrating,newtags,newlang,newprice,newpicblob,newdesc,newext,movindx)
        sql="UPDATE movie SET mname =?, genre=?, rating=?, tags=?, lang=?, price=?, photo=?, description=?, extt=? WHERE id=?"
        cursor.execute(sql,data)
        conn.commit()
        conn.close()
    except:
        conn.close()
        pass

# def editmovtablenopic(newven,newcap,newrat,newadd,newdesc,venindx,oldname):
def editmovtablenopic(newmov, newgenre, newrat, newtags, newlang, newprice, newdesc, movindx, oldmovname):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    # print('atleast this works')
    try:
        if oldmovname != newmov:
            inndata=(newmov,oldmovname)
            try:
                innsql="UPDATE show SET mname =? WHERE mname=?"
                cursor.execute(innsql,inndata)
            except:
                pass
            # print("vennname changed and the cascade thingie worked")
        data=(newmov, newgenre, newrat, newtags, newlang, newprice, newdesc, movindx)
        # sql="UPDATE venue SET vname =?, capacity=?, rating=?, address=?, description=?, WHERE id=?"
        sql="UPDATE movie SET mname =?, genre=?, rating=?, tags=?, lang=?, price=?, description=? WHERE id=?"
        # print("a satisfactory update to the venue table")
        cursor.execute(sql,data)
        conn.commit()
        conn.close()
    except:
        conn.close()
        pass


def editshowtable(venname,movname,dat,tim,showindx):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        # print("you're working really hard to not work")
        data=(movname,venname,dat,tim,showindx)
        sql="UPDATE show SET mname =?, vname=?, datee=?, timee=? WHERE id=?"
        # print("are you even trying?")
        cursor.execute(sql,data)
        # print("atleast im executing")
        conn.commit()
        conn.close()
        # print("Guess what? this worked")
    except:
        conn.close()
        # print("IG u found your bug")
        pass

def venuedeleter(venid):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        # print("you're working really hard to not work")
        data=(venid)
        sql="DELETE FROM venue WHERE id = ?"
        # print("are you even trying?")
        cursor.execute(sql,data)
        # print("atleast im executing")
        conn.commit()
        conn.close()
        # print("Guess what? this worked too")
    except:
        conn.close()
        # print("IG u found your bug")
        pass

def moviedeleter(movid):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        # print("you're working really hard to not work")
        data=(movid)
        sql="DELETE FROM movie WHERE id = ?"
        # print("are you even trying?")
        cursor.execute(sql,data)
        # print("atleast im executing")
        conn.commit()
        conn.close()
        # print("Guess what? this worked too")
    except:
        conn.close()
        # print("IG u found your bug")
        pass


def showdeleter(showid):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        # print("you're working really hard to not work")
        data=(showid)
        sql="DELETE FROM show WHERE id = ?"
        # print("are you even trying?")
        cursor.execute(sql,data)
        # print("atleast im executing")
        conn.commit()
        conn.close()
        # print("Guess what? this worked too")
    except:
        conn.close()
        # print("IG u found your bug")
        pass

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# print(show_finder())


def searchquery(query):
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, vname,mname FROM show")
        show_list = cursor.fetchall()
    except:
        show_list = []
    try:
        cursor.execute("SELECT id, mname, tags, genre FROM movie")
        movie_list = cursor.fetchall()
    except:
        movie_list = []
    try:
        cursor.execute("SELECT id, vname, address FROM venue")
        venue_list = cursor.fetchall()
    except:
        venue_list = []
    conn.close()
    matched_ven=[]
    matched_mov=[]
    matched_show_mov=[]
    matched_show_ven=[]
    available_ven, available_mov= ven_mov_finder()
    for i in venue_list:
        # print(i[1])
        score= fuzz.token_sort_ratio(query, str(i[1]))
        if score>50:
            matched_ven.append(i)
    print(matched_ven)

    for i in venue_list:
        # print(i[1])
        a=i[2].split()

        # this is code that should mapp to the address field
        for j in a:
            score= fuzz.token_sort_ratio(query, str(j))
            if score>50:
                matched_ven.append(i)
    print(matched_ven)

    matched_ven=list(set(matched_ven))

    for i in movie_list:
        # print(i[1])
        score= fuzz.token_sort_ratio(query, str(i[1]))
        if score>50:
            matched_mov.append(i)
    print(matched_mov)

    for i in movie_list:
        # print(i[1])
        a=i[2].split()

        # this is code that should mapp to the address field
        for j in a:
            score= fuzz.token_sort_ratio(query, str(j))
            if score>50:
                matched_mov.append(i)

    for i in movie_list:
        # print(i[1])
        a=i[3].split()

        # this is code that should mapp to the address field
        for j in a:
            score= fuzz.token_sort_ratio(query, str(j))
            if score>50:
                matched_mov.append(i)

    matched_mov=list(set(matched_mov))


    for i in show_list:
        # print(i)
        score = fuzz.token_sort_ratio(query, str(i[1]))
        if score > 50:
            for j in available_ven:
                # x=j[0]
                if i[1]==j[0]:
                    matched_show_ven.append(i)
    print(matched_show_ven)

    for i in show_list:
        # print(i)
        score = fuzz.token_sort_ratio(query, str(i[2]))
        if score > 50:
            for j in available_mov:
                # x = j[0]
                if i[2] == j[0]:
                    matched_show_mov.append(i)
    print(matched_show_mov)

    # print(f"Similarity score: {fuzz.token_sort_ratio(query, test)}")
    # print(venue_list,movie_list,show_list)
    main_ven_all_deets=ven_all_deets()
    main_mov_all_deets=mov_all_deets()
    main_show_all_deets=show_all_deets()
    fin_ven_deets=[]
    fin_mov_deets=[]
    fin_show_deets=[]
    print()
    print("------------------------")
    # print(main_ven_all_deets)
    # print(main_mov_all_deets)
    # print(main_show_all_deets)

    for i in matched_ven:
        ven_inxd=i[0]
        for j in main_ven_all_deets:
            if j[0]==ven_inxd:
                fin_ven_deets.append(j)
                break

    for i in matched_mov:
        # b=i
        mov_indx=i[0]
        for j in main_mov_all_deets:
            # a=j
            if j[0]==mov_indx:
                fin_mov_deets.append(j)
                break

    for i in matched_show_mov:
        a=i
        show_mov=i[0]
        for j in main_show_all_deets:
            b=j
            if j[0]==show_mov:
                fin_show_deets.append(j)
                break

    for i in matched_show_ven:
        a=i
        show_ven=i[0]
        for j in main_show_all_deets:
            b=j
            if j[0]==show_ven:
                fin_show_deets.append(j)
                break

    fin_show_deets=list(set(fin_show_deets))
    # todo: DONE the above for loop needs to be duplicated again and used for the lists 3 and 4 matched_show_ven and matched_show_mov



    # todo: DONE convert the list to a set and then back to a list. i dont really care for the order of the content, only the content itself.

    return (fin_ven_deets,fin_mov_deets,fin_show_deets)

# a,b,c=searchquery("maharashtra")
# print(c)

def booking_all_dets():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT book.id AS bookid, venue.vname AS vname, movie.mname AS mname, venue.id AS vid, movie.id AS mid, book.tim AS booktim, book.tickno AS toticks FROM book INNER JOIN show ON book.sindx = show.id INNER JOIN movie ON show.mname = movie.mname INNER JOIN venue ON show.vname = venue.vname")
        book_deets_list = cursor.fetchall()
    except:
        book_deets_list=[]

    conn.close()


    oldest=datetime.strptime(book_deets_list[0][5], "%Y-%m-%d %H:%M:%S.%f")
    latest=datetime.strptime(book_deets_list[0][5], "%Y-%m-%d %H:%M:%S.%f")
    for i in book_deets_list:
        time=datetime.strptime(i[5], "%Y-%m-%d %H:%M:%S.%f")
        if time>latest:
            latest=time
        elif time<oldest:
            oldest=time
    chunk=latest-oldest
    # chunk=chunk.total_seconds()
    division=chunk/5
    bar_1=oldest+division
    bar_2=bar_1+division
    bar_3=bar_2+division
    bar_4=bar_2+division
    x_axis=[str(oldest),str(bar_1),str(bar_2),str(bar_3),str(bar_4)]
    # print(oldest)
    # print(bar_1)
    # print(bar_2)
    # print(bar_3)
    # print(bar_4)
    # print(latest)
    # print("===========================")
    booking_1 = []
    booking_2 = []
    booking_3 = []
    booking_4 = []
    booking_5 = []
    master_booking=[]
    for i in book_deets_list:
        time=datetime.strptime(i[5], "%Y-%m-%d %H:%M:%S.%f")
        # print(i)
        # if time >oldest :
        #     booking_1.append(i)
        if time >=oldest and time<bar_1:
            booking_1.append(i)
        elif time >=bar_1 and time<bar_2:
            booking_2.append(i)
        elif time >=bar_2 and time<bar_3:
            booking_3.append(i)
        elif time >=bar_3 and time<bar_4:
            booking_4.append(i)
        elif time >=bar_4 and time<=latest:
            booking_5.append(i)
    master_booking=[booking_1,booking_2,booking_3,booking_4,booking_5]
    ven_list=[]
    mov_list=[]
    for i in book_deets_list:
        venue=i[1]
        movie=i[2]
        ven_list.append(venue)
        mov_list.append(movie)

    ven_list=list(set(ven_list))
    mov_list=list(set(mov_list))

    return(oldest,latest,chunk,division,master_booking,ven_list,mov_list,x_axis)

# print(booking_all_dets())
# booking_all_dets()
def venue_graph_func():
    oldest,latest,chunk,division,master_booking,ven_list,mov_list,x_axis=booking_all_dets()
    master_ven_booking=[]
    for i in master_booking:
        booking=[]
        for k in ven_list:
            ven=0
            for j in i:
                # print(j)
                if k==j[1]:
                    ven=ven+j[6]
            booking.append(ven)
        master_ven_booking.append(booking)
    print(ven_list)
    print(master_ven_booking)
    maxtick=0
    split_master_ven=[]
    for i in range(len(ven_list)):
        ven=[]
        for j in master_ven_booking:
            ven.append(j[i])
            if j[i]>maxtick:
                maxtick=j[i]
        split_master_ven.append(ven)
    print(split_master_ven)
    print(maxtick)
    for i in range(len(split_master_ven)):
        y=np.array(split_master_ven[i])
        # x=np.array([1,2,3,4,5])
        plt.plot(y,marker = 'o',ms = 10,linestyle = 'dotted', label=ven_list[i])

    plt.title("Popularity of Venues Overtime")
    leg = plt.legend(loc='upper center')
    plt.xlabel("Time")
    plt.ylabel("Number of Tickets Purchased")
    # plt.show()
    plt.savefig("./static/venuegraph.png")
    plt.clf()
    return split_master_ven, ven_list, maxtick, x_axis

# venue_graph_func()


def movie_graph_func():
    oldest,latest,chunk,division,master_booking,ven_list,mov_list,x_axis=booking_all_dets()
    master_mov_booking=[]
    for i in master_booking:
        booking=[]
        for k in mov_list:
            mov=0
            for j in i:
                if k==j[2]:
                    mov=mov+j[6]
            booking.append(mov)
        master_mov_booking.append(booking)
    # print(mov_list)
    # print(master_mov_booking)
    maxtick=0
    split_master_mov=[]
    for i in range(len(mov_list)):
        mov=[]
        for j in master_mov_booking:
            mov.append(j[i])
            if j[i]>maxtick:
                maxtick=j[i]
        split_master_mov.append(mov)
    # print(split_master_mov)
    # print(maxtick)
    print(len(split_master_mov))
    for i in range(len(split_master_mov)):
        y=np.array(split_master_mov[i])
        # x=np.array([1,2,3,4,5])
        print(mov_list[i])
        plt.plot(y,marker = 'o',ms = 10,linestyle = 'dotted', label=mov_list[i])

    plt.title("Popularity of Movies Overtime")
    leg = plt.legend(loc='upper center')
    plt.xlabel("Time")
    plt.ylabel("Number of Tickets Purchased")
    # plt.show()
    plt.savefig("./static/moviegraph.png")
    plt.clf()
    return split_master_mov, mov_list, maxtick,x_axis

# movie_graph_func()


