import sqlite3


def get_value_from_db(query: str):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()
        return result


def creation_of_list_of_movies(query):
    result = get_value_from_db(query)
    list_of_movies = []
    for item in result:
        list_of_movies.append(dict(item))

    return list_of_movies


# поиск фильма по названию
def search_movie_by_name(name: str) -> dict:
    query = f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE title = '{name}'
        AND release_year = (SELECT MAX(release_year) FROM netflix where title='{name}') 
        """
    result = get_value_from_db(query)
    for item in result:
        result = dict(item)

    return result


# поиск фильма по промежутку даты выхода
def search_movie_by_year(year_from, year_to):
    query = f"""
        SELECT release_year, title 
        FROM netflix
        WHERE release_year > {year_from} and release_year < {year_to}
        LIMIT 100
        """
    list_of_movies = creation_of_list_of_movies(query)
    return list_of_movies


# поиск фильма по возрастному рейтингу
def search_movies_by_rating(group: str):
    dictt = {
        'children': ('G', 'G'),
        'family': ('G', 'PG', 'PG-13'),
        'adult': ('R', 'NC-17')
    }

    query = f"""
          SELECT title, rating, description
          FROM netflix
          WHERE rating in {dictt.get(group)}

          """

    list_of_movies = creation_of_list_of_movies(query)
    return list_of_movies


# поиск фильма по жанру
def search_movies_by_genre(genre: str):
    query = f"""
              SELECT title, description
              FROM netflix
              WHERE listed_in like '%{genre}%'
              ORDER BY  release_year
              LIMIT 10
              """

    list_of_movies = creation_of_list_of_movies(query)
    return list_of_movies


# поиск фильма по актерам
def search_movies_by_actors(actor_1: str, actor_2: str):
    query = f"""
              SELECT title, description, "cast"
              FROM netflix
              WHERE "cast" like '%{actor_1}%' and "cast" like '%{actor_2}%'
              """

    list_of_movies = creation_of_list_of_movies(query)
    names_dict = {}

    for actors in list_of_movies:
        names = set(dict(actors).get('cast').split(',')) - set([actor_1, actor_2])

        for name in names:
            names_dict[str(name).strip()] = names_dict.get(str(name).strip(), 0) + 1

    double_movies = []
    for key, value in names_dict.items():
        if value >= 2:
            double_movies.append(key)

    return double_movies


def search_movie_by_criteries(type, release_year, genre):
    query = f"""
                 SELECT title, description, "type", release_year, listed_in 
                 FROM netflix
                 WHERE "type" like '%{type}%' 
                 and "listed_in" like '%{genre}%'
                 and release_year like '%{release_year}%'
                 """

    list_of_movies = creation_of_list_of_movies(query)
    return list_of_movies


# print(search_movies_by_actors('Rose McIver', 'Ben Lamb'))
for row in search_movie_by_criteries('Movie', 1978, 'Comedies'):
    print(row)