'''MovieLens Web Application'''
from database import MovieLensDB
import logging
import tornado.ioloop
import tornado.web
# Global values
PORT = 8888
# Handlers
class MainHandler(tornado.web.RequestHandler):
    '''Handles requests for the main page'''
    
    def initialize(self, db):
        self.db = db
        
    def get(self):
        genres = self.db.list_genres()
        movie_genres = []
        for item in genres:
            movie_genres.append(item['genre'])

        
        self.render('search_page.html', genres=movie_genres) 

class TitleSearchHandler(tornado.web.RequestHandler):
    '''Handles title search requests'''
    
    def initialize(self, db):
        self.db = db

    def get(self):
        title = self.get_argument('moviename')
        rows=db.search_title(title)
        
        self.render('movie_index.html', rows=rows)
        
class GenreSearchHandler(tornado.web.RequestHandler):
    '''Handles genre search requests'''
    def initialize(self, db):
        self.db = db
    
    def get(self):
        genre = self.get_argument('genre')
        rows= db.search_genre(genre)
        
        self.render('movie_index.html', rows=rows)
        
class DetailHandler(tornado.web.RequestHandler):
    '''Handles details for a single movie'''
    def initialize(self, db):
        self.db = db
    def get(self, movie_id):
        movie = self.db.movie_detail(movie_id)
        rating = self.db.get_rating(movie_id)
        imdbdata = self.db.imdb_data(movie['imdb_id'])
        genres = self.db.list_genres()
        movie_genres = []
        for item in genres:
            movie_genres.append(item['genre'])

        self.render('movie_detail.html', movie = movie, genres = movie_genres, rating = rating, imdb_data = imdbdata)
      

class RatingHandler(tornado.web.RequestHandler):
    '''Handles requests submitting new ratings'''
    
    def initialize(self, db):
          self.db = db
        
    def get(self):

        movie = self.get_argument("movie_id")
        rating = self.get_argument("rating")
        self.db.set_rating(movie,rating)

        self.redirect('/detail/{}'.format(movie))

# main code block
if __name__ == '__main__':

    db = MovieLensDB()
    
    app = tornado.web.Application([
            (r'/', MainHandler, {'db': db}),
            (r'/title', TitleSearchHandler, {'db':db}),
            (r'/genre', GenreSearchHandler, {'db': db}),
            (r'/detail/(\d+)', DetailHandler, {'db': db}),
            (r'/rating', RatingHandler, {'db': db}),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path':'assets/css'}),
        ],
        template_path = 'assets/templates',
        debug = True
    )

    # run the app
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()