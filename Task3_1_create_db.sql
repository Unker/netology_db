CREATE TABLE IF NOT EXISTS Artists (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Albums (
	id SERIAL primary key,
	title VARCHAR(80) NOT NULL,
	year DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Tracks (
	id SERIAL PRIMARY KEY,
	idAlbum INTEGER REFERENCES Albums(id),
	name VARCHAR(80) NOT NULL,
	timeDuration INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Collections (
	id SERIAL PRIMARY KEY,
	name VARCHAR(80) NOT NULL,
	year DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS StylesSong (
	id SERIAL PRIMARY KEY,
	styleName VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ArtistsAlbums (
	idArtist INTEGER REFERENCES Artists(id),
	idAlbum INTEGER REFERENCES Albums(id),
	constraint pkArtistsAlbums primary key (idArtist, idAlbum)
);

CREATE TABLE IF NOT EXISTS StylesArtists (
	idArtist INTEGER REFERENCES Artists(id),
	idStyle INTEGER REFERENCES StylesSong(id),
	constraint pkStylesArtists primary key (idArtist, idStyle)
);

CREATE TABLE IF NOT EXISTS CollectionsSongs (
	idCollection INTEGER REFERENCES Collections(id),
	idTrack INTEGER REFERENCES Tracks(id),
	constraint pkCollectionsSongs primary key (idCollection, idTrack)
);