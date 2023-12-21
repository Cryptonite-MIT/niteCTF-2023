const dotenv = require("dotenv");
const sqlite3 = require("sqlite3");
const nanoid = require("nanoid");

dotenv.config();

const sleep = (time) => {
    return new Promise(function (resolve) {
        setTimeout(resolve, time);
    });
};

const initUsersDb = () =>
    new Promise(async (resolve, reject) => {
        const db_users = new sqlite3.Database(
            `${process.env.DB_FOLDER}/users.db`
        );
        db_users.serialize(() => {
            db_users.run("DROP TABLE IF EXISTS USERS");
            db_users.run("CREATE TABLE USERS (username TEXT, hash TEXT)");
        });
        db_users.close();
        await sleep(500);

        resolve(true);
    });

const checkIfUserExists = (username) =>
    new Promise((resolve, reject) => {
        const db_users = new sqlite3.Database(
            `${process.env.DB_FOLDER}/users.db`
        );
        db_users.serialize(() =>
            db_users.all(
                "SELECT * FROM USERS WHERE username = ?",
                username,
                async (err, rows) =>
                    rows && rows.length !== 0
                        ? resolve(rows[0])
                        : resolve(false)
            )
        );
        db_users.close();
    });

const checkIfBookExists = (source, username, key) =>
    new Promise((resolve, reject) => {
        const db = new sqlite3.Database(
            `${process.env.DB_FOLDER}/${username}.db`
        );
        db.serialize(() => {
            if (source === "report")
                db.all(
                    "SELECT * FROM BOOKS WHERE liteId = ?",
                    key,
                    async (err, rows) => {
                        if (!rows) resolve(null);
                        else
                            rows.length !== 0
                                ? resolve(rows[0])
                                : resolve(false);
                    }
                );
            else if (source === "update")
                db.all(
                    "SELECT * FROM BOOKS WHERE title = ?",
                    key,
                    async (err, rows) => {
                        if (!rows) resolve(null);
                        else
                            rows.length !== 0
                                ? resolve(rows[0])
                                : resolve(false);
                    }
                );
            else if (source === "create")
                db.all("SELECT * FROM BOOKS", async (err, rows) => {
                    if (!rows) resolve(null);
                    else resolve(rows);
                });
            else resolve(null);
        });
        db.close();
    });

const checkUserPassword = (username, password) =>
    new Promise((resolve, reject) => {
        const db_users = new sqlite3.Database(
            `${process.env.DB_FOLDER}/users.db`
        );
        db_users.serialize(() =>
            db_users.all(
                "SELECT * FROM USERS WHERE username = ? AND hash = ?",
                username,
                password,
                async (err, rows) =>
                    rows && rows.length !== 0
                        ? resolve(rows[0])
                        : resolve(false)
            )
        );
        db_users.close();
    });

const addNewUserRecord = (username, hash) =>
    new Promise((resolve, reject) => {
        const db_users = new sqlite3.Database(
            `${process.env.DB_FOLDER}/users.db`
        );
        db_users.serialize(() => {
            const insertStatement = db_users.prepare(
                "INSERT INTO USERS VALUES (?, ?)"
            );
            insertStatement.run(username, hash);
            insertStatement.finalize();

            resolve(true);
        });
        db_users.close();
    });

const addNewUserBooks = (username, books = []) =>
    new Promise((resolve, reject) => {
        const db = new sqlite3.Database(
            `${process.env.DB_FOLDER}/${username}.db`
        );
        db.serialize(() => {
            db.run("DROP TABLE IF EXISTS BOOKS");
            db.run(
                "CREATE TABLE BOOKS (title TEXT, author TEXT, pages TEXT, imageLink TEXT, link TEXT, fav TEXT, read TEXT, liteId TEXT)"
            );

            const insertStatement = db.prepare(
                "INSERT INTO BOOKS VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            );
            books.forEach((book) => {
                const liteId = nanoid.nanoid(process.env.LENGTH_LITE_ID);

                insertStatement.run(
                    book.title,
                    book.author,
                    book.pages,
                    book.imageLink,
                    book.link,
                    username === "admin" ? Math.random() > 0.6 : false,
                    username === "admin" ? Math.random() > 0.3 : false,
                    liteId
                );
            });
            insertStatement.finalize();

            resolve(true);
        });
        db.close();
    });

module.exports = {
    initUsersDb,
    checkIfUserExists,
    checkIfBookExists,
    checkUserPassword,
    addNewUserRecord,
    addNewUserBooks,
};
