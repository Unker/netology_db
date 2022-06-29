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
print('Count tracks in the range from 2019 to 2020')
print(*tracksCount, sep = "\n")
print()

# средняя продолжительность треков по каждому альбому
meanDurations = connection.execute(f"""
	SELECT 
		a.title, CAST(AVG(t.timeDuration) AS decimal(16,2))
	FROM 
		Albums AS a
	LEFT JOIN Tracks AS t 
		ON a.id = t.idAlbum
	GROUP BY
		a.id
	;
	""").fetchall()
print('Mean duration tracks in each albums')
print(*meanDurations, sep = "\n")
print()

# все исполнители, которые не выпустили альбомы в 2020 году
artists = connection.execute(f"""
	SELECT 
		DISTINCT(ar.name)
	FROM 
		ArtistsAlbums AS aa
	JOIN Artists AS ar 
		ON aa.idArtist = ar.id
	JOIN Albums AS al 
		ON aa.idAlbum = al.id
	WHERE
		date_part('year', al.year) != 2020
	;
	""").fetchall()
print('The Artists who have not released albums in 2020')
print(*artists, sep = "\n")
print()

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
nameCollections = connection.execute(f"""
	SELECT 
		cl.name
	FROM 
		CollectionsSongs AS cs
	JOIN Collections AS cl 
		ON cs.idCollection = cl.id
	JOIN Tracks AS tr 
		ON cs.idTrack = tr.id
	JOIN Albums AS al 
		ON tr.idAlbum = al.id
	JOIN ArtistsAlbums AS aa 
		ON al.id = aa.idAlbum
	JOIN Artists AS ar 
		ON ar.id = aa.idArtist
	WHERE
		ar.name = 'best artist'
	;
	""").fetchall()
print('The collections in which present \"best artist\"')
print(*nameCollections, sep = "\n")
print()

# название альбомов, в которых присутствуют исполнители более 1 жанра
albums = connection.execute(f"""
	SELECT 
		al.title, COUNT(DISTINCT(sa.idStyle))
	FROM 
		Artists AS ar 
	JOIN ArtistsAlbums AS aa 
		ON ar.id = aa.idArtist
	JOIN Albums AS al  
		ON aa.idAlbum = al.id
	JOIN StylesArtists AS sa 
		ON ar.id = sa.idArtist
	GROUP BY
		al.title
	HAVING COUNT(DISTINCT(sa.idStyle)) > 1
	;
	""").fetchall()
print('The albums include artists of more than 1 Style')
print(*albums, sep = "\n")
print()

# наименование треков, которые не входят в сборники
tarcks = connection.execute(f"""
	SELECT 
		tr.name
	FROM 
		Tracks AS tr 
	LEFT JOIN CollectionsSongs AS cs 
		ON tr.id = cs.idTrack
	WHERE
		cs.idCollection IS NULL
	;
	""").fetchall()
print('The name of tracks that are not included in the collections')
print(*tarcks, sep = "\n")
print()

# исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
track = connection.execute(f"""
	SELECT 
		ar.name
	FROM 
		Tracks AS tr
	JOIN Albums AS al 
		ON al.id = tr.idAlbum
	JOIN ArtistsAlbums AS aa 
		ON al.id = aa.idAlbum
	JOIN Artists AS ar 
		ON ar.id = aa.idArtist
	WHERE 
		tr.timeDuration = (
			SELECT 
				MIN(timeDuration)
			FROM 
				Tracks
		)
	;
	""").fetchall()
print('The artist(s) who wrote the shortest track in duration')
print(*track, sep = "\n")
print()

# название альбомов, содержащих наименьшее количество треков
albums = connection.execute(f"""
	SELECT 
		al.title
	FROM
		Albums AS al
	JOIN Tracks AS tr 
		ON al.id = tr.idAlbum
	GROUP BY
		al.title
	HAVING 
		COUNT(tr.idAlbum) = (SELECT MIN(cnt)
			FROM (
				SELECT 
					COUNT(tr.idAlbum) as cnt
				FROM 
					Albums AS al
				JOIN Tracks AS tr 
					ON al.id = tr.idAlbum
				GROUP BY
					al.title
			) AS x
	)

	;
	""").fetchall()
print('The albums containing the least number of tracks')
print(*albums, sep = "\n")
print()
