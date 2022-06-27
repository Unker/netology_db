import sqlalchemy
from pprint import pprint

dbname = 'mydb'
user = 'demo_netology'
dbpass = 'pass'
host='localhost'
port = '5432'
db = f'postgresql://{user}:{dbpass}@{host}:{port}/{dbname}'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


# название и год выхода альбомов, вышедших в 2018 году
albums = connection.execute(f"""
	SELECT title, date_part('year', year)::numeric::integer
	FROM Albums
	WHERE date_part('year', year) = 2018;
	""").fetchall()
print('Albums realized in 2018')
pprint(albums)
print()

# название и продолжительность самого длительного трека
track = connection.execute(f"""
	SELECT name, timeDuration
	FROM Tracks
	WHERE timeDuration = (
		SELECT MAX (timeDuration)
		FROM Tracks
	)
	;
	""").fetchall()
print('Track with max duration')
pprint(track)
print()

# название треков, продолжительность которых не менее 3,5 минуты
tracks = connection.execute(f"""
	SELECT name, timeDuration
	FROM Tracks
	WHERE timeDuration >= 3.5*60
	;
	""").fetchall()
print('Tracks with the duration of more than 3.5 min')
pprint(tracks)
print()

# названия сборников, вышедших в период с 2018 по 2020 год включительно
collections = connection.execute(f"""
	SELECT name
	FROM Collections
	WHERE date_part('year', year) >= 2018 
	AND date_part('year', year) <= 2020
	;
	""").fetchall()
print('Collections from 2018 to 2020 years')
pprint(collections)
print()

# исполнители, чье имя состоит из 1 слова
artists = connection.execute(f"""
	SELECT name
	FROM Artists
	WHERE name NOT LIKE '%% %%';
	;
	""").fetchall()
print('Artists with a single word name')
pprint(artists)
print()

# название треков, которые содержат слово "мой"/"my"
tracks = connection.execute(f"""
	SELECT name
	FROM Tracks
	WHERE name LIKE '%%my%%';
	;
	""").fetchall()
print('Tracks that contain \"my\"')
pprint(tracks)
print()