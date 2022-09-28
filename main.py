from utils import *
import flask


app = flask.Flask(__name__)


@app.get('/movie/<title>')
def search_by_title(title):
    return search_movie_by_name(title)


@app.get('/movie/<year_1>/to/<year_2>')
def search_by_year(year_1, year_2):
    return search_movie_by_year(year_1, year_2)


@app.get('/rating/<rating>')
def search_by_rating(rating):
    return search_movies_by_rating(rating)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)