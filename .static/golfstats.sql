CREATE TABLE location (locationid SERIAL PRIMARY KEY,
                       locationname VARCHAR(100),
                       address VARCHAR(100),
                       city VARCHAR(50));

CREATE TABLE golfcourse (golfcourseid SERIAL PRIMARY KEY,
                         locationid INT,numholes INT,
                         name VARCHAR(100),
                         FOREIGN KEY (locationid) REFERENCES location (locationid));

CREATE TABLE golfhole (golfholeid SERIAL PRIMARY KEY,
                       golfcourseid INT,length INT,
                       par INT,
                       number INT,
                       FOREIGN KEY (golfcourseid) REFERENCES golfcourse (golfcourseid));

CREATE TABLE player (playerid SERIAL PRIMARY KEY,
                     firstname VARCHAR(20),
                     lastname VARCHAR(30),
                     email VARCHAR(100) );

CREATE TABLE round (roundid SERIAL PRIMARY KEY,
                    golfcourseid INT,
                    dateplayed DATE,
                    FOREIGN KEY (golfcourseid) REFERENCES golfcourse (golfcourseid) );

CREATE TABLE playerround (playerroundid SERIAL PRIMARY KEY,
                          roundid INT,
                          golfcourseid INT,
                          playerid INT,
                          totalscore INT,
                          FOREIGN KEY (roundid) REFERENCES round (roundid),
                          FOREIGN KEY (golfcourseid) REFERENCES golfcourse (golfcourseid),
                          FOREIGN KEY (playerid) REFERENCES player (playerid));

CREATE TABLE score (scoreid SERIAL PRIMARY KEY,
                    playerroundid INT,
                    golfholeid INT,
                    strokes INT,
                    FOREIGN KEY (playerroundid) REFERENCES playerround (playerroundid),
                    FOREIGN KEY (golfholeid) REFERENCES golfhole (golfholeid));

CREATE TABLE friendship (friendshipid SERIAL PRIMARY KEY,
                         playerid1 INT,
                         playerid2 INT,
                         status VARCHAR(20),
                         friendshipdate DATE,
                         FOREIGN KEY (playerid1) REFERENCES player (playerid),
                         FOREIGN KEY (playerid2) REFERENCES player (playerid));