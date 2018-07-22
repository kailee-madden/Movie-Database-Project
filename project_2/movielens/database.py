#!/usr/bin/env python
'''Interface for the movielens database'''

# import statements
import sqlite3
import os
import requests

# class definitions
class MovieLensDB(object):
    '''A connection to the MovieLens database'''

    DATA_DIR = 'assets/data'
    DB_FILE = os.path.join(DATA_DIR, 'movielens.db')
    TABLES = ['Movie', 'GenreTag', 'Rating']
    
    
    def __init__(self, db_file=DB_FILE, data_dir=DATA_DIR):
        '''Initialize a new database connection'''

        self.db_file  = db_file
        self.data_dir = data_dir
        self.conn     = sqlite3.connect(db_file)
         
        # set some database parameters
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
       

        self._create_tables()
        self._populate_tables()
        
    
    def _create_tables(self):
        '''Execute the SQL commands in sql_file to create tables'''

        cur = self.conn.cursor()

        cur.execute('''
        DROP TABLE IF EXISTS GenreTag
        ''')  
        cur.execute('''
        DROP TABLE IF EXISTS Rating
        ''')    
        cur.execute('''
        DROP TABLE IF EXISTS Movie
        ''')  

        # create the Movie, GenreTag, and Rating tables    
        
        create_movie =  '''
        CREATE TABLE IF NOT EXISTS Movie(
            movie_id    INTEGER PRIMARY KEY,
            title       TEXT,
            year        INTEGER,
            imdb_id     INTEGER
            )
            ''' 
        cur.execute(create_movie)

        create_genre =  '''
        CREATE TABLE IF NOT EXISTS GenreTag(
            gtag_id     INTEGER PRIMARY KEY,
            movie_id    INTEGER,
            genre       TEXT,
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
            )
            ''' 

        cur.execute(create_genre)

        create_rating =  '''
        CREATE TABLE IF NOT EXISTS Rating(
            rating_id   INTEGER PRIMARY KEY,
            movie_id    INTEGER,
            rating      INTEGER,
            FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
            )
            ''' 
        cur.execute(create_rating)

        cur = self.conn.cursor()
        
    
    
    def _populate_tables(self):
        '''Populate the tables using local TSV data'''
        
        # source files for table data
        movie_file  = os.path.join(self.data_dir, 'movies.tsv')
        genre_file  = os.path.join(self.data_dir, 'genres.tsv')
        rating_file = os.path.join(self.data_dir, 'ratings.tsv')
                
        cur = self.conn.cursor()


        movie_sql = '''
        INSERT INTO Movie VALUES (:movie_id, :title, :year, :imdb_id)
        '''

        with open(movie_file) as fh:
            fh.readline()
            for line in fh:
                    rec = line.strip().split('\t')
                    cur.execute(movie_sql, rec)

        genre_sql = '''
        INSERT INTO GenreTag VALUES (NULL, :movie_id, :genre)
        '''

        with open(genre_file) as fh:
            fh.readline()
            for line in fh:
                    rec = line.strip().split('\t')
                    cur.execute(genre_sql, rec)

        rating_sql = '''
        INSERT INTO Rating VALUES (NULL, :movie_id, :rating)
        '''
        with open(rating_file) as fh:
            fh.readline()
            for line in fh:
                rec = line.strip().split('\t')
                cur.execute(rating_sql, rec)
        
        self.conn.commit()
    
    def search_title(self, title):
        '''Return a list of movies that match title'''

        cur = self.conn.cursor()
        
        sql = '''
        SELECT 
            movie_id,
            title,
            year 
        FROM 
            Movie
        WHERE
            title
        LIKE ?
        ORDER BY
            title,
            year,
            movie_id
        '''
        
        cur.execute(sql, ('%' + title + '%',))
        return cur.fetchall()
    
    def search_genre(self,genre):
        '''Return a list of movies tagged with a genre'''
        
        cur = self.conn.cursor()

        sql =  'SELECT Movie.movie_id, title, year FROM GenreTag JOIN Movie ON GenreTag.movie_id = Movie.movie_id WHERE genre LIKE ?'

        cur.execute(sql, (genre,))
        return cur.fetchall()
    
    def movie_detail(self, movie_id):
        '''Return details for a single movie'''
        
        cur = self.conn.cursor()
        
        sql = 'SELECT title, year, imdb_id, movie_id FROM Movie WHERE movie_id == ?'
        
        cur.execute(sql, (movie_id,))        
        return cur.fetchone()

    def get_rating(self, movie_id):
        '''return the average rating for a specific movie'''
        
        cur = self.conn.cursor()
        
        sql = 'SELECT AVG(rating) AS rating, COUNT(rating) AS count FROM Rating WHERE movie_id == ?'
        
        cur.execute(sql, (movie_id,))   
        return cur.fetchone()

    def get_genres(self, movie_id):
        '''Return the list of genres for a specific movie'''
    
        cur = self.conn.cursor()
        
        sql = 'SELECT genre FROM GenreTag WHERE movie_id == ?'
        
        cur.execute(sql, (movie_id,))
        return cur.fetchall()
    
    def set_rating(self, movie_id, rating):
        '''Add a user rating for a movie'''
        
        cur = self.conn.cursor()

        sql = 'INSERT INTO Rating Values (Null, :movieid, :rating)'
        cur.execute(sql, (movie_id, rating,))
        return cur.fetchall()

    def list_genres(self):
        '''List all distinct genre tags in the database'''
        
        cur = self.conn.cursor()
        
        sql = 'SELECT DISTINCT genre FROM GenreTag ORDER BY genre'
        
        cur.execute(sql)
        return cur.fetchall()
    
    def imdb_data(self, imdb_id):
        '''Query the Open Movie Database for extra metadata'''
        
        URL = 'http://www.omdbapi.com/?i={}'.format(imdb_id)
        res = requests.get(URL)
        if res.ok:
            return res.json()