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


# количество исполнителей в каждом жанре
stylesCount = connection.execute(f"""
	SELECT 
		s.styleName, COUNT(sa.idArtist)
	FROM 
		StylesSong AS s
	INNER JOIN StylesArtists AS sa 
		ON s.id = sa.idStyle
	GROUP BY
		s.id
	;
	""").fetchall()
print('Number of Artists in each styles')
print(*stylesCount, sep = "\n")
print()

# количество треков, вошедших в альбомы 2019-2020 годов
tracksCount = connection.execute(f"""
	SELECT 
		COUNT(t.id)
	FROM 
		Albums AS a
	INNER JOIN Tracks AS t 
		ON t.idAlbum = a.id
	WHERE
		date_part('year', a.year) >= 2019 
		AND date_part('year', a.year) <= 2020

	;
	""").fetchall()
print('Number of Artists in each styles')
print(*tracksCount, sep = "\n")
print()