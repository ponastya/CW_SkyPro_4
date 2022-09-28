import sqlite3



def get_value_from_db(query: str):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()
        return result


def search_movie_by_name(name) -> dict:
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


def search_movie_by_year(year_from, year_to):
    query = f"""
        SELECT release_year, title 
        FROM netflix
        WHERE release_year > {year_from} and release_year < {year_to}
        LIMIT 100
        """
    result = get_value_from_db(query)
    list_of_movies = []
    for item in result:
        result = dict(item)
        list_of_movies.append(result)
    return list_of_movies