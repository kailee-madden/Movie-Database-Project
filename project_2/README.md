# MovieLens Database

This project uses the MovieLens dataset from the University of Minnesota. It
consists of a large set of movies, with associated genre tags and viewer
ratings. Our goals are to

 - organize this data in an SQLite database

 - create basic search functionality for title and genre-based searches

 - create functionality for registering new ratings

 - build a web frontend for our application using Tornado


## Skeleton code

The structure of the application is laid out in the code provided. It's up to
you to fill in the specified `TODO` sections to create the functionality and 
build the interface.

    movielens/
       database.py           # the database functionality
       web.py                # the tornado web app
    assets/
       templates/
           search_page.html  # the app home page, with search form
           movie_index.html  # the results page, listing matching movies
           movie_detail.html # details for a specific movie
                             #    - including rating submission form
      data/
         genres.tsv          # genre data
         movies.tsv          # movie data
         ratings.tsv         # ratings data
      css/
         style.css           # a stylesheet placeholder
         

## Outline of tasks

### database.py

This module supplies all the database operations for the app. Add code to the **MovieLensDB** class -- in areas marked `TODO` -- to implement the following functionality.

1. `__init__()`

    - use sqlite3 to connect to the database `/assets/data/movielens.db`
     
    - set appropriate instance variables
    
    - call `_create_tables`
   
    - call `_populate_tables`
   
2. `_create_tables()`

    - delete the tables **Rating**, **GenreTag**, **Movie** if they exist
    
        - hint: delete **Movie** last to avoid integrity errors

    - create the tables anew, with the following columns
    
        - **Movie**
        
            - *movie_id*  (Primary Key)
            
            - *title*
            
            - *year*
            
        - **GenreTag**
        
            - *gtag_id*  (Primary Key)
            
            - *movie_id* (Foreign Key)
            
            - *genre*
            
        - **Rating**
        
            - *rating_id* (Primary Key)
            
            - *movie_id*  (Foreign Key)
            
            - *rating*
            
    - The **GenreTag** and **Rating** tables should have foreign keys on *movie_id*, referencing *movie_id* in **Movie**.
    
3. `_populate_tables()`

    - populate the tables using the respective data files
    
    - data are TSV
    
       - remember to drop the header line
       
       - remember to strip the newline character
       
    - for **Movie** use the *movie_id* provided in the data
    
    - for the other two tables, use `NULL` for the primary key and let
      SQLite provide a value
      
4. `search_title()`

    - This takes one argument, a string, and performs a search on the *title*
      column of the **Movie** table, using `LIKE` to capture inexact matches.

    - returns a list of `Row` objects with the following columns
    
       - *movie_id*
       
       - *title*
       
       - *year*
       
    - you might want to sort the results
    
5. `search_genre()`

    - This takes one argument, a string
    
    - Performs a search on the *genre* column of the **GenreTag** table
    
    - Combined with a `JOIN` on the **Movie** table to retrieve all the movies
      tagged with a certain genre
      
    - Use `==` instead of `LIKE` for exact match only.

    - returns a list of `Row` objects with the same columns as (4) above
    
6. `movie_detail()`

    - This takes one argument, a movie id
    
    - Searches the **Movie** table for an exact match on *movie_id*
    
    - Returns a single Row, with the following columns
    
       - *movie_id*
       
       - *title*
       
       - *year*
       
       - *imdb_id*

7. `get_rating()`

    - This takes one argument, a movie id
    
    - Performs a search of the **Rating** table
    
    - Returns a row with two columns
    
       - the **average** of the *rating* column for all rows matching 
         *movie_id*, renamed as `rating`
       
       - the **count** of rows matching the *movie_id* column, renamed as 
         `count`
    
    - That is, the average rating and the number of people who rated the movie

8. `get_genres()`

    - This takes one argument, a movie id
    
    - Performs a search of the **GenreTag** table for rows matching *movie_id*
    
    - Returns a list of Row objects, each with a single column, `genre`
    
9. `set_rating()`

    - This takes two arguments, a movie id, and a rating (between 1 and 5)
    
    - Adds a new row to the **Rating** table, storing the movie rating
    
10. `list_genres()`

    - This takes no arguments
    
    - Does a search of the **GenreTag** table for all distinct values for the *genre* column
    
    - Returns a list of Row objects, each with a single column, `genre`
    
    - again, think about sorting
    
11. `imdb_data()`

    - **You don't have to do anything here**
    
    - This method takes a single argument, a movie id
    
    - Performs an internet search to retrieve additional metadata about the
      movie from the [Open Movie Database](http://www.omdbapi.com)
      
    - Returns a dictionary with some interesting tidbits, including
    
        - `Plot` - a brief summary of the movie
        
        - `Poster` - a URL pointing to a remote image
    
    - These will come in handy building your **Detail Page** 
    

### web.py

This script creates the app and serves it. Add code to the `TODO` areas to implement the following functionality.

#### Handlers

1. `MainHandler`

    - This serves requests for the root URL (`/`)
    
    - calls the `get_genres()` method to find out which genres are available
    
    - renders the `search_page.html` template
    
2. `TitleSearchHandler`

    - This serves requests for `/title`
    
    - retrieves a user-supplied *title* and calls `search_title()`
    
    - renders `movie_index.html` to display the results (see minimum 
      requirements below)
    
3. `GenreSearchHandler`

    - This serves requests for `/genre`
    
    - retrieves a user-supplied *genre* and calls `search_genre()`
    
    - renders `movie_index.html` to display the results, as in (2)
    
4. `DetailHandler`

    - This servers requests for `/detail`
    
    - retrieves a user-supplied *movie_id* and calls 
    
       - `movie_detail()`
       
       - `get_genres()`
       
       - `get_rating()`
       
       - `imdb_data()`
    
    - renders `movie_detail.html` to display the results (see minimum
      requirements below)
      
5. `RatingHandler`

    - This serves requests for `/rating`
    
    - retrieves two user-supplied values, a *movie_id* and a *rating*,
      and calls `set_rating()`
      
    - then **redirects** back to the detail page
    
6. main code block

    - create a new database object using `MovieLensDB`

    - register the URLS specified above with their respective handlers
    
    - remember to pass the database object to the Handlers
    
### Templates

These build the web interface, using values supplied by the handlers where 
necessary. They should include **at least** the following elements and 
functionality, but you are expected also to show some creativity.

1. `search_page.html`

   - set the page `<title>`
     
   - create an `<h1>` with a header for the page
     
   - create two `<form>` elements:
     
       - one does a title search

           - has `/title` as its `action`
           
           - contains a text `<input>` for the user-supplied title
           
       - one does a genre search
       
           - has `/genre` as its `action`
           
           - only lets the user choose from existing genres
           
2. `movie_index.html`

   - set the page `<title>`
     
   - create an `<h1>` with a header for the page

   - display a list of movie records, for example as table rows
   
   - for each movie, provide **at least** the following
   
       - title
       
       - year
       
       - link to **detail page**
       
3. `movie_detail.html`

    - set the page `<title>`
     
    - create an `<h1>` with a header containing the movie *title*
      
    - display **at least** the following details about the movie
    
        - image from imdb
        
        - plot summary from imdb
        
        - user rating from the `get_rating()` method
        
        - genre tags from the `get_genres()` method
        
    - create a form allowing user to submit a rating
    
        - action is `/rating`
                
        - let the user choose a *rating* between 1 and 5
        
        - hint: you can use `<input type="hidden">` to store the *movie_id*
