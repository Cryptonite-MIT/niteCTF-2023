const data = require("./data.json");
const sqlite3 = require("sqlite3");

const db = new sqlite3.Database("chalSqlite.db");

db.serialize(() => {
    db.run("DROP TABLE IF EXISTS BOOKS");
    db.run(
        "CREATE TABLE BOOKS (title TEXT, author TEXT, pages TEXT, imageLink TEXT, link TEXT)"
    );
    const insertStatement = db.prepare(
        "INSERT INTO BOOKS VALUES (?, ?, ?, ?, ?)"
    );

    data["books"].forEach((book) => {
        insertStatement.run(
            book.title,
            book.author,
            book.pages,
            book.imageLink,
            book.link
        );
    });

    insertStatement.finalize();
    console.log("DB: Books ready");
});

db.serialize(() => {
    db.run("DROP TABLE IF EXISTS USERS");
    db.run(
        "CREATE TABLE USERS (liteId TEXT, liteUsername TEXT, gender TEXT, liteNick TEXT, litePass TEXT, dateCreated TEXT)"
    );
    const insertStatement = db.prepare(
        "INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?)"
    );

    data["users"].forEach((user) => {
        insertStatement.run(
            user.id,
            user.username,
            user.gender,
            user.nick,
            user.password,
            user.dateCreated
        );
    });

    insertStatement.finalize();
    console.log("DB: Users ready");
});

db.close();
