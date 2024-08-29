DROP TABLE admins;
DROP TABLE head_admins;
DROP TABLE elements;
DROP TABLE photography;


CREATE TABLE admins (
    id TEXT,
    username TEXT,
    password TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE head_admins (
    id TEXT,
    FOREIGN KEY (id) REFERENCES admins(id)    
);



CREATE TABLE elements (
    id TEXT,
    title TEXT NOT NULL,
    desciption TEXT,
    type TEXT CHECK (type = 'cultures' OR type = 'articles'),
    date NUMERIC DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE photography(
    id NUMERIC,
    title TEXT,
    desciption TEXT,
    date NUMERIC DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
    );
INSERT INTO head_admins (id) VALUES ('Ri3JXVWwwgcdqq3wzrzD');
INSERT INTO admins (id, username,password) VALUES ('Ri3JXVWwwgcdqq3wzrzD','Nomad','scrypt:32768:8:1$p21ZWE1dXfvZSlB1$9eb63acbecd3df3c2593e91ed57d09e29e336cdf21a6f0905cabc1c23ba55394f18372f60ee0c932053b8b2ea58d740938bceea43cad2128b2e8767f1cf85494');