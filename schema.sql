
CREATE TABLE Users (
    id TEXT,
    username TEXT UNIQUE,
    password TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE Admins (
    id TEXT,
    FOREIGN KEY (id) REFERENCES Users(id)
);
CREATE TABLE Writters (
    id TEXT,
    FOREIGN KEY (id) REFERENCES Users(id)
);


CREATE TABLE Articles (
    id TEXT,
    title TEXT NOT NULL,
    desciption TEXT,
    date NUMERIC DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
CREATE TABLE Tags (
    id INTEGER,
    name TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE Categorize (
    article_id TEXT,
    tag_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES Articles(id),
    FOREIGN KEY (tag_id) REFERENCES Tags(id)
);

CREATE TABLE Actions (
    article_id TEXT,
    user_id TEXT,
    type TEXT CHECK (type = 'write' OR type = 'edit' OR type = 'delete'),
    date NUMERIC DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES Articles(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
INSERT INTO Users (id, username,password) VALUES ('Ri3JXVWwwgcdqq3wzrzD','Nomad','scrypt:32768:8:1$p21ZWE1dXfvZSlB1$9eb63acbecd3df3c2593e91ed57d09e29e336cdf21a6f0905cabc1c23ba55394f18372f60ee0c932053b8b2ea58d740938bceea43cad2128b2e8767f1cf85494');
INSERT INTO Admins (id) VALUES ('Ri3JXVWwwgcdqq3wzrzD');
INSERT INTO Tags (name) VALUES ('History');
INSERT INTO Tags (name) VALUES ('Palestine 101');
INSERT INTO Tags (name) VALUES ('Religion');
INSERT INTO Tags (name) VALUES ('Massacres');
INSERT INTO Tags (name) VALUES ('Zioni Myths');
INSERT INTO Tags (name) VALUES ('Nekba');
INSERT INTO Tags (name) VALUES ('Int Law');
INSERT INTO Tags (name) VALUES ('War Crimes');
INSERT INTO Tags (name) VALUES ('Identity');
INSERT INTO Tags (name) VALUES ('Protests');
INSERT INTO Tags (name) VALUES ('BDS');
INSERT INTO Tags (name) VALUES ('Culture');
INSERT INTO Tags (name) VALUES ('Nationalism');
INSERT INTO Tags (name) VALUES ('Human Rights');
INSERT INTO Tags (name) VALUES ('Zioni Quotes');
INSERT INTO Tags (name) VALUES ('Solutions');
INSERT INTO Tags (name) VALUES ('Naksa');
INSERT INTO Tags (name) VALUES ('Palestine Quotes');
INSERT INTO Tags (name) VALUES ('Hasbara Tactic');



