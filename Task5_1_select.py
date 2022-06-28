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
styles = connection.execute(f"""
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
print(*styles, sep = "\n")
print()