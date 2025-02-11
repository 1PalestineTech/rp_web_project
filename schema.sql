
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

CREATE TABLE Editors (
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
    id TEXT,
    name TEXT,
    PRIMARY KEY(id)
);
CREATE TABLE Categorize (
    article_id TEXT,
    tag_id TEXT,
    FOREIGN KEY (article_id) REFERENCES Articles(id),
    FOREIGN KEY (tag_id) REFERENCES Tags(id)
);

CREATE TABLE Action (
    article_id TEXT,
    user_id TEXT,
    type TEXT CHECK (type = 'write' OR type = 'edit' OR type = 'delete'),
    date NUMERIC DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES Articles(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
INSERT INTO Users (id, username,password) VALUES ('Ri3JXVWwwgcdqq3wzrzD','Nomad','scrypt:32768:8:1$p21ZWE1dXfvZSlB1$9eb63acbecd3df3c2593e91ed57d09e29e336cdf21a6f0905cabc1c23ba55394f18372f60ee0c932053b8b2ea58d740938bceea43cad2128b2e8767f1cf85494');
INSERT INTO Admins (id) VALUES ('Ri3JXVWwwgcdqq3wzrzD');
INSERT INTO Tags (name,id) VALUES ('History','ZkSDkwPr1H2EIzb3Zjwh');
INSERT INTO Tags (name,id) VALUES ('Culture','F4zV58GF2SVC3xaTW8C6');
INSERT INTO Tags (name,id) VALUES ('Massacres','dAQOKHq5KKtEv9jdjJgr');
INSERT INTO Tags (name,id) VALUES ('Current Event','qxedzb2sh6Drd5dC6t3L');
INSERT INTO Tags (name,id) VALUES ('Facts','dTChIrJ047TKMlZaKb3I');




