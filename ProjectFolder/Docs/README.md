This is an overview of the ticket booking system TicketGenie.

### Login Functions:
##### Register new user:
A user can user the register button to register as a new user for the website. Here he has the option to become an admin or not. Also the username and email have to be unique and not used previously.

##### Login users/admins:
Both users and admins have the same login platform. If the username and password are correct they are redirected to their respective profile pages

##### Logout:
To end a session, the user has to logout from the website. Unless a user is logged out he cannot login or register a new user.


### Admin Functions:
##### Admin Profile Page:
This is the main page from which the admin can manage all venues/movies/shows. New venues/movies/shows can be added, edited and deleted from here. This page also links to the admin dashboard.

##### Creating a new venue/movie:
An admin can create a new venue/movie and provide all custom details. Here the photo option is the only optional attribute, and if a photo is not provided a default photo is selected from the backed. 

##### Creating a new show:
Since a show is a combination of a movie and a venue, this page provided dropdowns for both values which are extracted from the backed. The admin provides a date and time for the show and the publishes it.

##### Edit a venue/movie/show:
An admin can edit a venue/movie/show by clicking on the respective button on the admin profile. From here the previous entered data is extracted from the backed and autofilled. The admin can now edit this data. If a new photo is not provided, the previously saved photo is used.

##### Delete a venue/movie/show:
On the edit page, the admin has the ability to delete the movie/venue/show. These deletions cascade and affect the entire database to ensure consistency and integrity of the system.

##### Bookings Summary:
The admin profile has a button on its top left called Dashboard. The dashboard provides a dynamic visualization of the booking that have taken place over the entire period and divides bookings onto 5 sections. These sections are then plotted separately for movies and venues thus providing an overview of how a movie/venue is performing overtime especially with respect to other movies and venues.


### User Functions:
##### User Profile Page:
The user profile page is used to display all the past bookings of the user. This allows the user to have an overview of the bookings that have been made. Also here the user can rate movies and venues.
##### Book Tickets For Shows:
The user can book tickets for a specific instance of a show. This redirects the user to the specific url for that specific show. Here he can see the details of the booking including the venue, movie, available seats, price per seat. Also the user can select the number of tickets he/she wants to book as long as its less or equal to the number of available tickets. The total price dynamically displays the price (= single price * no of tickets booked).

##### Rate Movies/Venues:
On the users profile page, the users can rate the movies and venues associated with the shows that they have booked. If a user has made multiple bookings for a single venue/movie, each booking will have the option to rate their respective venues & movies thus leading to duplicate rating abilities. However the most recent rating for that specific movie or venue by that user is considered.


### Functions For All:
##### Home page:
The homepage (visible to all) is a collection of all shows that are currently available. These shows are grouped by venues and only allow the ability to book a ticket to users (not admins).

##### Search:
The Search system is available for all users even those not logged in. Here the user can search movies/venues/shows via tags/genres/addresses/names/titles/etc etc. It returns the most relevant search results again classified on the basis of movies venues and shows.

##### View Venue/Movie Details:
By clicking on the venue/movie on the homepage, the user can be redirected to a page that displays more detailed information about a the respective venue/movie. This allows the user to explore more about the place/movie. Also on these pages, the current shows associated with the venue/movie via a show are displayed. 

