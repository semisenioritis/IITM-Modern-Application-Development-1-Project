from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename
import os
import userdb as dbs



import adminfunc as adb
import userfunc as udb

app = Flask(__name__)
app.secret_key= "hello"

@app.route('/')
def main_func():
    showslist = adb.show_finder()
    shows_indx_list = udb.show_finder_ven_indx()
    showlistlen=[]
    # print("wazzzzap")
    for i in range(len(shows_indx_list)):
        # print(i)
        # showlistlen.append(i)

        if len(shows_indx_list[i]) !=0:
            showlistlen.append(i)
    # print("show list length  ",showlistlen)
    # print("wazzzzzzup")
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        admin = user_data[0][4]
        # print("meeee")
        # print("show list  ",showslist)
        # print("show index list  ",shows_indx_list)
        # print("meeee")
        if admin == 1:
            admin = "Admin"
        else:
            admin = "User"
        return render_template("index.html", username=user, admin_stat=admin, showslist=showslist, showindxlist=shows_indx_list, showlistlen=showlistlen)
    else:
        return render_template("index.html",username="",admin_stat="", showslist=showslist, showindxlist=shows_indx_list, showlistlen=showlistlen)

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["unm"]
        password=request.form["pwd"]
        # session is a dictionary that stores the details of the current user inlcuding the email and the username etc etc
        if dbs.login(user, password)== True:
            session['user'] = user
            user_data = dbs.check_data_exists_in_table("users", "username", user)
            admin = user_data[0][4]
            if admin == 1:
                admin = "Admin"
                return redirect(url_for("admin_profile"))

            else:
                admin = "User"
                return redirect(url_for("user_profile"))


            # once you actually login correctly this is what renders after the POST action.
        else:
            # todo: make this page a bit more better
            return f"<h1>Invalid username or password</h1>"

    else:
        if "user" in session:
            user = session['user']
            user_data = dbs.check_data_exists_in_table("users", "username", user)
            admin = user_data[0][4]
            # print(user_data)
            if admin == 1:
                admin = "Admin"
                return redirect(url_for("admin_profile"))

            else:
                admin = "User"
                return redirect(url_for("user_profile"))
            # if the user is already logged in but tries to acess the login page this redirects them to their so called "profile" page
        else:
            return render_template("login.html")
        # the first thing that gets rendered in this system. this page is the landing page for the login system

@app.route("/uprofile")
def user_profile():
    if "user" in session:
        user=session['user']
        user_data=dbs.check_data_exists_in_table("users","username",user)
        # print(user_data)
        admin=user_data[0][4]
        myind=user_data[0][0]
        my_bookings= udb.user_bookings_retriever(myind)
        # print(my_bookings)
        shows_indx_list = udb.show_finder_ven_indx()
        # print(shows_indx_list)

        mov_indx_list_reshuffled=[]
        for i in my_bookings:
            flag = 0
            for j in shows_indx_list:
                if i[6]==j[0][2]:
                    mov_indx_list_reshuffled.append(j[0])
                    flag=1
                    # print(i[6],j[0][2])
            if flag==0:
                mov_indx_list_reshuffled.append((0, 'Null ', 'Null', 1, 1))
        # print(mov_indx_list_reshuffled)

        # print("comeon wassup danger")
        # print(my_bookings[0])
        for i in range(len(my_bookings)):
            mov_inddd=mov_indx_list_reshuffled[i][4]
            temp=list(my_bookings[i])
            temp.append(mov_inddd)
            temp= tuple(temp)
            my_bookings[i]=temp
        # print("like wasssup danger")


        # print("comeon wassup danger")
        # print(my_bookings[0])
        for i in range(len(my_bookings)):
            ven_inddd=mov_indx_list_reshuffled[i][3]
            temp=list(my_bookings[i])
            temp.append(ven_inddd)
            temp= tuple(temp)
            my_bookings[i]=temp
        # print("like wasssup danger")

        # Right now i just added two more indices to each element in the my_bookings list
        # these indices are 1: the movie index of teh booking & 2: the venue index of the booking respectively



        if admin==1:
            admin="Admin"
        else:
            admin="User"
        return render_template("user_profile.html",username=user,admin_stat=admin, my_bookings=my_bookings)
        # the profile page of the individual user
    else:
        return redirect(url_for("login"))
        # if the user login is not valid at the current moment, rediret him to the login page

@app.route("/aprofile")
def admin_profile():
    if "user" in session:
        user=session['user']
        user_data=dbs.check_data_exists_in_table("users","username",user)
        admin=user_data[0][4]
        if admin==1:
            admin="Admin"
        else:
            admin="User"
        venuelist= adb.ven_all_deets()
        movielist= adb.mov_all_deets()
        showslist= adb.show_finder()
        # print()
        # print("wassuppppppppppppp")
        # print(venuelist)
        # print(movielist)
        # print(showslist)
        # print("wassuppppppppppppp")
        return render_template("admin_profile.html",username=user,admin_stat=admin, venuelist=venuelist, movielist=movielist, showslist=showslist)
        # the profile page of the individual user
    else:
        return redirect(url_for("login"))
        # if the user login is not valid at the current moment, rediret him to the login page

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user = request.form["unm"]
        password=request.form["pwd"]
        uemail = request.form["email"]
        admin = request.form.get("admin")
        if admin == "on":
            admin = 1
        else:
            admin = 0
        # print(user)
        # print(password)
        # print(uemail)
        # print(admin)
        # print(bool(dbs.check_data_exists_in_table("users","username",user)))
        # print(bool(dbs.check_data_exists_in_table("users","email",uemail)))
        # print(not(bool(dbs.check_data_exists_in_table("users","username",user))) and not(bool(dbs.check_data_exists_in_table("users","email",uemail))))
        if (not(bool(dbs.check_data_exists_in_table("users","username",user))) and not(bool(dbs.check_data_exists_in_table("users","email",uemail))))==True:
            # print("this is unique")

            anss=dbs.register(user, password, uemail, admin)
            # print("reg done")
            if anss== True:
                session['user'] = user
                # print("reg worked")
                if admin == 1:
                    admin = "Admin"
                    return redirect(url_for("admin_profile"))

                else:
                    admin = "User"
                    return redirect(url_for("user_profile"))

            # once you actually login correctly this is what renders after the POST action.
        else:
            # todo: make this page a bit more better
            return f"<h1>The username/emailid might alredy be taken</h1>"

    else:
        if "user" in session:
            user = session['user']
            user_data = dbs.check_data_exists_in_table("users", "username", user)
            admin = user_data[0][4]
            if admin == 1:
                admin = "Admin"
                return redirect(url_for("admin_profile"))

            else:
                admin = "User"
                return redirect(url_for("user_profile"))
            # if the user is already logged in but tries to acess the login page this redirects them to their so called "profile" page
        else:
            return render_template("register.html")
        # the first thing that gets rendered in this system. this page is the landing page for the login system

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
    # the url to log the user out


@app.route("/newvenue", methods=["POST", "GET"])
def venue_creator():
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        admin = user_data[0][4]
        if admin == 1:
            admin="Admin"
            # print("i am admin")
            if request.method == "POST":
                # print("post just happened")
                venname = str(request.form["vnam"])
                maxcap = int(request.form["capacity"])
                rating = int(request.form["rating"])
                add = str(request.form["add"])
                desc=str(request.form["desc"])
                file = request.files["photo"]

                # print(file)
                # print(file.filename)
                temp_name = secure_filename(file.filename.replace(" ", ""))
                ext=str(temp_name.split(".")[-1])
                tmpname=secure_filename("temp."+str(ext))
                tmpname= "static/"+tmpname
                # print(tmpname)

                if str(file.filename)=="":
                    tmpname="static/blankvenue.jpg"
                    ext="jpg"
                else:
                    file.save(tmpname)

                # print(tmpname)


                # print("i think the image got saved")

                # todo: DONE do not allow to post empty input
                image_path = tmpname
                # todo: DONE if photo not there image_path= some default image
                # photo.save(image_path)
                # todo: DONE store photo in a local place.
                picblob= adb.convertToBinaryData(image_path)
                # todo: DONE delete the file that just got created
                if tmpname!="static/blankvenue.jpg":
                    os.remove("./"+tmpname)
                # todo: DONE convert photo to blob and push resulting blob into the database function bellow
                # todo: DONE if no photo is selected, select the default photo make a copy, blobify it and then pass that into the venuecreator
                adb.venue_creator(venname, maxcap, rating, add, picblob, desc, ext)
                return redirect(url_for("admin_profile"))

            else:

                print("i can see venue adder")
                return render_template("new_venue.html", username=user, admin_stat=admin)
        else:
            print("i cant see venue adder")
            return redirect(url_for("user_profile"))


    else:
        print("i am not logged in")
        return redirect(url_for("login"))


@app.route("/newmovie", methods=["POST", "GET"])
def movie_creator():
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        admin = user_data[0][4]
        if admin == 1:
            admin="Admin"
            print("i am admin")
            if request.method == "POST":
                print("post just happened")
                movname = str(request.form["mnam"])
                genre = str(request.form["genres"])
                rating = int(request.form["rating"])
                tags = str(request.form["tags"])
                language= str(request.form["lang"])
                price= int(request.form["price"])
                desc = str(request.form["desc"])
                file = request.files["photo"]

                print(file)
                print(file.filename)
                temp_name = secure_filename(file.filename.replace(" ", ""))
                ext = str(temp_name.split(".")[-1])
                tmpname = secure_filename("temp." + str(ext))
                tmpname = "static/" + tmpname
                print(tmpname)


                if str(file.filename)=="":
                    tmpname="static/blankmovie.jpg"
                    ext="jpg"
                else:
                    file.save(tmpname)

                print(tmpname)
                print("i think the image got saved")

                # todo: DONE do not allow to post empty input
                image_path = tmpname
                picblob= adb.convertToBinaryData(image_path)
                if tmpname!="static/blankmovie.jpg":
                    os.remove("./"+tmpname)

                # print(movname,genre,rating,tags,language,price)
                # print(type(movname),type(genre),type(rating),type(tags),type(language),type(price))
                adb.movie_creator(movname,genre,rating,tags,language,price, picblob, desc, ext)
                print("i dont know if pushing worked, but now i should be redirected to admin page")
                return redirect(url_for("admin_profile"))

            else:

                print("i can see venue adder")
                return render_template("new_movie.html", username=user, admin_stat=admin)
        else:
            print("i cant see venue adder")
            return redirect(url_for("user_profile"))


    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/newshow", methods=["POST", "GET"])
def show_creator():
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        admin = user_data[0][4]
        if admin == 1:
            admin="Admin"
            print("i am admin")
            if request.method == "POST":
                print("post just happened")
                venname = str(request.form["venue"])
                movename = str(request.form["movie"])
                dat = str(request.form["showdate"])
                tim = str(request.form["showtime"])

                # print(movename, venname, dat, tim)
                # print(type(venname),type(movename),type(dat),type(tim))
                # adb.venue_creator(venname, maxcap, rating, add)
                adb.show_creator(movename,venname,dat,tim)

                return redirect(url_for("admin_profile"))

            else:

                print("i can see venue adder")
                ven_list,mov_list = adb.ven_mov_finder()
                print(ven_list[0][0])
                return render_template("new_show.html", username=user, admin_stat=admin, ven_list=ven_list, mov_list=mov_list)

        else:
            print("i cant see venue adder")
            return redirect(url_for("user_profile"))


    else:
        print("i am not logged in")
        return redirect(url_for("login"))


@app.route("/bookshow/<showid>", methods=["POST", "GET"])
def bookingsys(showid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 0:
            admin= "User"
            all = adb.show_all_deets()
            showid = int(showid)
            # myshow = all[showid]
            myshow=0
            for i in all:
                if i[0]== showid:
                    myshow= i

            movv = myshow[1]
            all_mov = adb.mov_all_deets()
            curr_cost=0
            for i in all_mov:
                if i[1] == movv:
                    curr_cost = i[6]
            if request.method == "POST":
                print("post just happened")
                userid= user_data[0][0]
                showindex = showid
                # todo: DONE REMEMBER THAT THE SHOW INDEX HERE REFERS TO THE INDEX IN TERMS OF LIST. NOT THE NUMBER..... MIGHT NEED TO CHANGE THIS LATER ON
                # todo: DONE yup changed this for the joins
                ticketnos = int(request.form["tickets"])
                totprice = ticketnos * int(curr_cost)
                print(userid,showindex,ticketnos,totprice)
                book_stat= udb.booking_creator(userid,showindex,ticketnos,totprice)
                if book_stat== True:
                    udb.reduce_seats(ticketnos,showindex)
                return redirect(url_for("user_profile"))
            else:
                print("i can see booking page")
                return render_template("confirm_booking.html", username=user, admin_stat=admin, myshow=myshow, curr_cost=curr_cost, showid=showid)


        else:
            print("i cant book tickets")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))


@app.route("/editvenue/<venid>", methods=["POST", "GET"])
def editvenue(venid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin= "Admin"
            all = adb.ven_all_deets()
            venid = int(venid)
            # myven = all[venid]
            myven=0
            for i in all:
                if i[0]== venid:
                    myven= i

            # print(myven)
            if request.method == "POST":
                print("post just happened")

                venname = str(request.form["vnam"])
                maxcap = int(request.form["capacity"])
                rating = int(request.form["rating"])
                add = str(request.form["add"])

                oldvenname=myven[1]
                venindx=venid


                file= request.files["photo"]
                print(file)
                print(file.filename)
                temp_name = secure_filename(file.filename.replace(" ", ""))
                ext=str(temp_name.split(".")[-1])
                tmpname=secure_filename("temp."+str(ext))
                tmpname= "static/"+tmpname
                print(tmpname)
                desc = str(request.form["desc"])

                if str(file.filename)=="":
                    adb.editventablenopic(venname, maxcap, rating, add, desc, venindx, oldvenname)
                    # todo: DONE call a different function that actually doesnt overwrite the og photo blob
                else:
                    print("i am getting called")
                    file.save(tmpname)
                    image_path = tmpname
                    picblob = adb.convertToBinaryData(image_path)
                    if tmpname!="static/blankvenue.jpg":
                        os.remove("./"+tmpname)
                    # todo: DONE edit bellow function to accomodate for changes
                    adb.editventable(venname, maxcap, rating, add, picblob, desc, ext, venindx, oldvenname)
                    # print(venname,maxcap,rating,add, desc,ext,venindx, oldvenname)
                    # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")


                return redirect(url_for("admin_profile"))
            else:
                print("i can see editing page")
                return render_template("edit_venue.html", username=user, admin_stat=admin, myven=myven,venid=venid) #showid=showid)


        else:
            print("i cant edit venue")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))


@app.route("/editmovie/<movid>", methods=["POST", "GET"])
def editmovie(movid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin= "Admin"
            all = adb.mov_all_deets()
            movid = int(movid)
            # mymov = all[movid]
            mymov=0
            for i in all:
                if i[0]== movid:
                    mymov= i

            print(mymov)
            if request.method == "POST":
                print("post just happened")

                movname = str(request.form["mnam"])
                genre = str(request.form["genres"])
                rating = int(request.form["rating"])
                tags = str(request.form["tags"])
                language= str(request.form["lang"])
                price= int(request.form["price"])

                oldmovname=mymov[1]
                movindx=movid


                file= request.files["photo"]
                print(file)
                print(file.filename)
                temp_name = secure_filename(file.filename.replace(" ", ""))
                ext=str(temp_name.split(".")[-1])
                tmpname=secure_filename("temp."+str(ext))
                tmpname= "static/"+tmpname
                print(tmpname)
                desc = str(request.form["desc"])

                if str(file.filename)=="":
                    # adb.editventablenopic(venname, maxcap, rating, add, desc, venindx, oldvenname)
                    adb.editmovtablenopic(movname, genre, rating, tags, language, price, desc, movindx, oldmovname)
                    # TODO: DONE ISKO MODIFY KAR JARA PLS. SAMJHA NA TU?

                else:
                    print("i am getting called")
                    file.save(tmpname)
                    image_path = tmpname
                    picblob = adb.convertToBinaryData(image_path)
                    if tmpname!="static/blankmovie.jpg":
                        os.remove("./"+tmpname)
                    # todo: DONE edit bellow function to accomodate for changes
                    # adb.editventable(venname, maxcap, rating, add, picblob, desc, ext, venindx, oldvenname)
                    adb.editmovtable(movname, genre, rating, tags, language, price, picblob, desc, ext, movindx, oldmovname)
                    # print(venname,maxcap,rating,add, desc,ext,venindx, oldvenname)
                    # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")





                # adb.editmovtable(movname,genre,rating,tags,language,price,movindx,oldmovname)
                return redirect(url_for("admin_profile"))
            else:
                print("i can see editing page")
                return render_template("edit_movie.html", username=user, admin_stat=admin, mymov=mymov,movid=movid)


        else:
            print("i cant edit movie")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))


@app.route("/editshow/<showid>", methods=["POST", "GET"])
def editshow(showid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin= "Admin"
            all = adb.show_all_deets()
            showid = int(showid)
            # myshow = all[showid]
            myshow=0
            for i in all:
                if i[0]== showid:
                    myshow= i

            ven_list, mov_list = adb.ven_mov_finder()
            print(myshow)
            if request.method == "POST":
                print("post just happened")
                venname = str(request.form["venue"])
                movname = str(request.form["movie"])
                dat = str(request.form["showdate"])
                tim = str(request.form["showtime"])
                showindx=showid
                # todo: DONE modify this
                # todo: DONE push this data to the table
                adb.editshowtable(venname,movname,dat,tim,showindx)
                return redirect(url_for("admin_profile"))
            else:
                print("i can see editing page")
                return render_template("edit_show.html", username=user, admin_stat=admin, myshow=myshow,showid=showid, ven_list=ven_list, mov_list=mov_list )


        else:
            print("i cant edit movie")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/deletevenue/<venid>", methods=["POST", "GET"])
def delven(venid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin= "Admin"
            adb.venuedeleter(venid)
            return redirect(url_for("admin_profile"))
        else:
            print("i cant delete")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/deletemovie/<movid>", methods=["POST", "GET"])
def delmov(movid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin= "Admin"
            adb.moviedeleter(movid)
            return redirect(url_for("admin_profile"))
        else:
            print("i cant delete")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/deleteshow/<showid>", methods=["POST", "GET"])
def delshow(showid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin= "Admin"
            adb.showdeleter(showid)
            return redirect(url_for("admin_profile"))
        else:
            print("i cant delete")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/vendisp/<venid>")
def vendisp(venid):
    all = adb.ven_all_deets()
    venid = int(venid)
    myven = 0
    for i in all:
        if i[0] == venid:
            myven = i
    photoblob = myven[5]
    fileext = myven[7]
    filenameee = "static/temp." + str(fileext)
    udb.writeTofile(photoblob, filenameee)
    our_rating=udb.ven_our_rating(venid)
    if our_rating==0:
        our_rating="-NA-"


    showslist = adb.show_finder()
    print(len(showslist))
    print(showslist)

    title=myven[1]
    print(title)
    fin_showslist=[]
    for i in showslist:
        print(i)
        ven_holder=[]
        for j in i:

            if j[2]==title:
                ven_holder.append(j)
        if len(ven_holder)!=0:
            fin_showslist.append(ven_holder)

    showslist=fin_showslist
    print(showslist)




    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin = "Admin"
        else:
            admin = "User"

        return render_template("display_venue.html", username=user, admin_stat=admin, myven=myven, venid=venid, photopath=filenameee, our_rating=our_rating,showslist=showslist)



    else:
        print("i am not logged in")
        return render_template("display_venue.html", username="", admin_stat="", myven=myven, venid=venid, photopath=filenameee, our_rating=our_rating,showslist=showslist)

@app.route("/movdisp/<movid>")
def movdisp(movid):
    all = adb.mov_all_deets()
    movid = int(movid)
    mymov = 0
    for i in all:
        if i[0] == movid:
            mymov = i
    photoblob = mymov[7]
    fileext = mymov[9]
    filenameee = "static/temp." + str(fileext)
    udb.writeTofile(photoblob, filenameee)
    our_rating=udb.mov_our_rating(movid)
    if our_rating==0:
        our_rating="-NA-"
    # todo: DONE once i revamp the db ill be able to do above thing

    showslist = adb.show_finder()
    print(len(showslist))
    print(showslist)

    title=mymov[1]
    print(title)
    fin_showslist=[]
    for i in showslist:
        ven_holder=[]
        for j in i:
            if j[1]==title:
                ven_holder.append(j)
        if len(ven_holder)!=0:
            fin_showslist.append(ven_holder)

    showslist=fin_showslist
    print(showslist)

    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin = "Admin"
        else:
            admin = "User"

        # todo: DONE change bellow thing after db revamp
        return render_template("display_movie.html", username=user, admin_stat=admin, mymov=mymov, movid=movid, photopath=filenameee, our_rating=our_rating,showslist=showslist)
        # return render_template("display_movie.html", username=user, admin_stat=admin, mymov=mymov, movid=movid)




    else:
        print("i am not logged in")

        # todo: DONE change bellow thing after db revamp
        return render_template("display_movie.html", username="", admin_stat="", mymov=mymov, movid=movid, photopath=filenameee, our_rating=our_rating,showslist=showslist)
        # return render_template("display_movie.html", username="", admin_stat="", mymov=mymov, movid=movid)

@app.route("/search/<query>")
def searcher(query):
    # todo: DONEcall the searchquery fucntion that uses the query parameter and searches stuff
    # todo: DONE now that i am able to find the ids of the data i need, i have to complete the function to retrieve the detils of these things and display them like the home page
    venue_details,movie_details,show_details=adb.searchquery(query)
    # print(venue_details)
    print(movie_details)
    print(show_details)
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 1:
            admin = "Admin"
        else:
            admin = "User"


        return render_template("search.html", username=user, admin_stat=admin, query=query, venue_details=venue_details,movie_details=movie_details,show_details=show_details)
    else:
        print("i am not logged in")
        return render_template("search.html", username="", admin_stat="", query=query, venue_details=venue_details,movie_details=movie_details,show_details=show_details)

@app.route("/ratemov/<movid>", methods=["POST"])
def ratemov(movid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 0:
            admin= "User"

            data = request.get_json()
            print("this is my data:")
            print(data)
            userid=user_data[0][0]
            curmovid=data["movid"]
            movrat=data["rating"]
            # print(curmovid,movrat)
            udb.movierater(userid,curmovid,movrat)

            # todo: DONE call the rate movie function here that takes the user id and the movie id and pushes it to the db
            return redirect(url_for("user_profile"))
        else:
            print("i cant delete")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/rateven/<venid>", methods=["POST"])
def rateven(venid):
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        print(user_data)
        admin = user_data[0][4]
        if admin == 0:
            admin= "User"

            data = request.get_json()
            print("this is my data:")
            print(data)
            userid=user_data[0][0]
            curvenid=data["venid"]
            venrat=data["rating"]
            # print(curvenid,venrat)
            udb.venuerater(userid,curvenid,venrat)

            # todo: DONE call the rate venue function here that takes the user id and the venue id and pushes it to the db
            return redirect(url_for("user_profile"))
        else:
            print("i cant delete")
            return redirect(url_for("main_func"))
    else:
        print("i am not logged in")
        return redirect(url_for("login"))

@app.route("/summary")
def summary():
    if "user" in session:
        user = session['user']
        user_data = dbs.check_data_exists_in_table("users", "username", user)
        admin = user_data[0][4]
        if admin == 1:
            admin="Admin"
            print("i am admin")
            adb.movie_graph_func()
            adb.venue_graph_func()

            # todo: DONE do the computation for generating the graph here. then pass that graph on to hte frontend and reender the url
            print("i can see summary")
            # todo: DONE modify the bottom render template too
            return render_template("summary.html", username=user, admin_stat=admin)

        else:
            print("i cant see summary")
            return redirect(url_for("user_profile"))

    else:
        print("i am not logged in")
        return redirect(url_for("login"))


if __name__=="__main__":
    app.run(debug=True)