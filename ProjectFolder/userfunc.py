from classes import Booking
import sqlite3
import datetime



def booking_creator(userindx,showindx,notick,totp):
    currbooking= Booking(userindx,showindx,notick,totp)
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)

    conn.execute('''CREATE TABLE IF NOT EXISTS book
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uindx INTEGER NOT NULL,
                    sindx INTEGER NOT NULL,
                    tickno INTEGER NOT NULL,
                    tot INTEGER NOT NULL,
                    tim TEXT NOT NULL);''')

    cur_time = str(datetime.datetime.now())
    # print(str(cur_time))
    cursor = conn.cursor()
    data = (currbooking.user_index, currbooking.show_index, currbooking.no_of_tickets, currbooking.total_price, cur_time)
    try:
        cursor.execute('INSERT INTO book (uindx, sindx, tickno, tot, tim) VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
        # print("i just sucessfully pushed a booking into the db")
        return True
    except:
        conn.close()
        # print("booking pushing didnt work")
        return False


def user_bookings_retriever(userindex):
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM book INNER JOIN show ON book.sindx= show.id WHERE uindx=?",(userindex,))
        all_booking_deets_list = cursor.fetchall()
        # print(all_booking_deets_list)
        conn.close()
    except:
        all_booking_deets_list=[]
        conn.close()
        pass
    return all_booking_deets_list

def reduce_seats(seatssold, showindx):
    conn = sqlite3.connect('dynamic.db', check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT rem_seat FROM show WHERE id=?",(showindx,))
        rem_list = cursor.fetchall()
        # print(vnam)
        # print(cap_list)
        # print(cap_list[0][0])
        rem_list = rem_list[0][0]
        rem_list=rem_list-seatssold
        data=(rem_list,showindx)
        sql="UPDATE show SET rem_seat =? WHERE id=?"
        cursor.execute(sql,data)
        conn.commit()


        conn.close()
    except:
        conn.close()
        pass

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    # print("Stored blob data into: ", filename, "\n")


def show_finder_ven_indx():
    conn = sqlite3.connect('dynamic.db')
    cursor = conn.cursor()
    try:
        # print("im gonna try")
        cursor.execute("SELECT DISTINCT vname FROM show")
        show_place_list = cursor.fetchall()
        # print("i tried a bit")
        # print("this is the result of me trying")
        # print(show_place_list)
        # print(show_place_list)
        # print(show_place_list_fin)
        super_show_list=[]

        for i in show_place_list:
            # print("im still trying")
            # print(i)
            # cursor.execute("SELECT * FROM show WHERE vname=? ",i)
            cursor.execute("SELECT show.id AS showid, venue.vname AS vname, movie.mname AS mname, venue.id AS vid, movie.id AS mid FROM movie INNER JOIN show ON movie.mname = show.mname INNER JOIN venue ON show.vname = venue.vname WHERE show.vname=? ",i)
            # todo: DONE replace above EXECUTE statement with the appropriate statement that extracts from venue table: id , movie table: id and show table : vname, mname and show id.
            # todo: DONE this table then lateron can be used to mapp venue display pages to the index.html so the user can click on the venue titles and see the venue pages.
            # SELECT table1.column1, table2.column2, table3.column3 FROM table1 INNER JOIN table2 ON table1.column1 = table2.column2 INNER JOIN table3 ON table2.column3 = table3.column4;

            # print("whooo if i dont get printed the above thing sucks")
            each_venue_show_deets_sub_list=cursor.fetchall()
            # print(each_venue_show_deets_sub_list)

            # listofshowsinvenue=cursor.fetchall()
            # print(each_venue_show_deets_sub_list)
            super_show_list.append(each_venue_show_deets_sub_list)
        # print(super_show_list)
        conn.close()
    except:
        # print("i tried and failed")
        super_show_list=[]
        conn.close()

    return (super_show_list)


def movierater(userid, movid, rating):
    conn = sqlite3.connect('ratings.db', check_same_thread=False)

    conn.execute('''CREATE TABLE IF NOT EXISTS movierating
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uid INTEGER NOT NULL,
                    movieid INTEGER NOT NULL,
                    rating INTEGER NOT NULL);''')

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM movierating")
        all_mov_rat = cursor.fetchall()

    except:
        all_mov_rat=[]

    done_flag=0
    for i in all_mov_rat:
        this_mov=i[2]
        this_user=i[1]
        if str(this_mov)==str(movid) and str(this_user)==str(userid):
            try:
                data= (rating,userid, movid)
                sql = "UPDATE movierating SET rating =? WHERE uid=? AND movieid=?"
                cursor.execute(sql, data)
                conn.commit()
                done_flag=1
                # print("existing was updated")
            except:
                # print("some error occured")
                done_flag=1
                pass
    if done_flag==0:
        try:
            data = (userid, movid, rating)
            sql="INSERT INTO movierating (uid, movieid, rating) VALUES (?, ?, ?)"
            cursor.execute(sql, data)
            conn.commit()
            # print("new was pushed")
        except:
            # print("some error occured")
            pass
    conn.close()

def venuerater(userid, venid, rating):
    conn = sqlite3.connect('ratings.db', check_same_thread=False)

    conn.execute('''CREATE TABLE IF NOT EXISTS venuerating
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uid INTEGER NOT NULL,
                    venueid INTEGER NOT NULL,
                    rating INTEGER NOT NULL);''')

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM venuerating")
        all_ven_rat = cursor.fetchall()

    except:
        all_ven_rat=[]

    done_flag=0
    for i in all_ven_rat:
        this_ven=i[2]
        this_user=i[1]
        if str(this_ven)==str(venid) and str(this_user)==str(userid):
            try:
                data= (rating,userid, venid)
                sql = "UPDATE venuerating SET rating =? WHERE uid=? AND venueid=?"
                cursor.execute(sql, data)
                conn.commit()
                done_flag=1
                # print("existing was updated")
            except:
                # print("some error occured")
                done_flag=1
                pass
    if done_flag==0:
        try:
            data = (userid, venid, rating)
            sql="INSERT INTO venuerating (uid, venueid, rating) VALUES (?, ?, ?)"
            cursor.execute(sql, data)
            conn.commit()
            # print("new was pushed")
        except:
            # print("some error occured")
            pass
    conn.close()

def ven_our_rating(venid):
    conn = sqlite3.connect('ratings.db')
    cursor = conn.cursor()
    try:
        data=(venid,)
        sql="SELECT rating FROM venuerating WHERE venueid=?"
        cursor.execute(sql, data)
        ven_rat_list = cursor.fetchall()
        conn.close()
        fin_ven_rat_list=[]
        for i in ven_rat_list:
            rat=i[0]
            fin_ven_rat_list.append(rat)
        ven_rat_list=fin_ven_rat_list
    except:
        ven_rat_list=[]
        conn.close()
        pass
    totrats=len(ven_rat_list)
    calc_rating=0
    if totrats==0:
        pass
    else:
        for i in ven_rat_list:
            calc_rating=calc_rating+i
        calc_rating=calc_rating//totrats

    return (calc_rating)

def mov_our_rating(movid):
    conn = sqlite3.connect('ratings.db')
    cursor = conn.cursor()
    try:
        data=(movid,)
        sql="SELECT rating FROM movierating WHERE movieid=?"
        cursor.execute(sql, data)
        mov_rat_list = cursor.fetchall()
        conn.close()
        fin_mov_rat_list=[]
        for i in mov_rat_list:
            rat=i[0]
            fin_mov_rat_list.append(rat)
        mov_rat_list=fin_mov_rat_list
    except:
        mov_rat_list=[]
        conn.close()
        pass
    totrats=len(mov_rat_list)
    calc_rating=0
    if totrats==0:
        pass
    else:
        for i in mov_rat_list:
            calc_rating=calc_rating+i
        calc_rating=calc_rating//totrats

    return (calc_rating)
# show_finder_ven_indx()
# reduce_seats(5,1)

