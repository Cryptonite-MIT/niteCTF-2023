const express = require("express");
const sqlite3 = require("sqlite3");
const bcrypt = require("bcrypt");
const dotenv = require("dotenv");
const cookieParser = require("cookie-parser");
const morgan = require("morgan");
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const nanoid = require("nanoid");
const net = require("net");

const utils = require("./utils.js");
const db = require("./utilsDb.js");

let PORT;
if (process.argv[2]) PORT = process.argv[2];
else {
    console.log("Exiting as listening port not provided");
    process.exit();
}

dotenv.config();

const DEBUG = false;
const SAMPLE_BOOKS_LIMIT = 7;
const MAX_VIEWABLE_BOOKS_LIMIT = 9;
const REGEX_UNAME = "[a-z\\d]{5,30}";
const REGEX_PASSWD = '[a-zA-Z\\d\\s"@#$%^&*\'"]{5,60}';
const ASSETS_CACHE_TIME_SECONDS = 1800;
const JWT_TOKEN_EXPIRY_SECONDS = 1800;
const BOT_HOST = "xss-bot.default.svc.cluster.local";
// const BOT_HOST = "127.0.0.1";
const SELF_HOST = "http://litelibrary-v2.web.nitectf.live";
// const SELF_HOST = "http://localhost:1338";

const MAX_INPUT_LENGTH = 4000;
const MAX_NUM_INPUT_LENGTH = 5;
const MAX_BOOK_COUNT = 20;
const BACKEND_ERROR_MSG =
    "Internal server error: contact ctf admin if this occurs repeatedly";
const ADMIN_LOCKED_MSG =
    "My lord I will never disobey you, even if it be you asking me to disobey. Your books stay locked forever.";

const reUname = new RegExp(`^${REGEX_UNAME}$`);
const rePass = new RegExp(`^${REGEX_PASSWD}$`);

require("./initDb.js");
const books = require("./books.json");

const app = express();
let countBooks = require("./startingData")["users"][0]["books"].length;

app.set("view engine", "ejs");

app.disable("x-powered-by");

app.use(
    "/assets",
    express.static("assets", {
        maxAge: `${ASSETS_CACHE_TIME_SECONDS * 1000}`,
    })
);

// logging
app.use(
    morgan(
        `:remote-addr ":user-agent" ":method :url HTTP/:http-version" :status - :res[content-length] bytes - :response-time ms`
    )
);

app.use(
    helmet({
        contentSecurityPolicy: {
            directives: {
                "default-src": ["'self'", "openlibrary.org"],
                "img-src": [
                    "'self'",
                    "raw.githubusercontent.com",
                    "external-content.duckduckgo.com",
                ],
                "script-src": null,
                "script-src-attr": null,
                "upgradeInsecureRequests": null,
            },
        },
    })
);

// /register RATE LIMITED TO 5 request for 5 minutes
// because new DB file created for every signup
const limiter_reg = rateLimit({
    windowMs: 5 * 60 * 1000,
    max: 5,
});
app.use("/register", limiter_reg);

// /report RATE LIMITED TO 6 request for 2 minutes
const limiter_report = rateLimit({
    windowMs: 2 * 60 * 1000,
    max: 6,
});
app.use("/report", limiter_report);

// RATE LIMITED TO 1 RPS; resets every minute
const limiter = rateLimit({
    windowMs: 60 * 1000,
    max: 60,
});
app.use("/api", limiter);

// RATE LIMITED TO 5 RPS; resets every 5 minutes
const limiter_lax = rateLimit({
    windowMs: 5 * 60 * 1000,
    max: 5 * 300,
});
app.use("/getBooks", limiter_lax);
app.use("/view", limiter_lax);

app.use(cookieParser());

app.use(express.json());
app.use(function (err, req, res, next) {
    if (err.type === "entity.parse.failed")
        res.status(400).send({ status: "error", msg: "Invalid input" });
    else next(err);
});

app.get("/", utils.authCheck, async (req, res) => {
    return res.render("index", {
        maxInputLength: MAX_INPUT_LENGTH,
    });
});

app.get("/stats", utils.authCheck, (req, res) => {
    return res.send({ status: "ok", count: countBooks - (countBooks % 10) });
});

app.get("/login", utils.authCheck, async (req, res) => {
    return res.render("login");
});

app.get("/register", utils.authCheck, async (req, res) => {
    return res.render("register", {
        regexUname: REGEX_UNAME,
        regexPasswd: REGEX_PASSWD,
    });
});

app.post("/register", async (req, res) => {
    let input_uname = req.query.username;
    let input_password = req.query.password;

    if (!input_uname || !input_password)
        return res
            .status(400)
            .send({ status: "error", msg: "All fields are mandatory" });

    if (!reUname.test(input_uname) || !rePass.test(input_password))
        return res.status(400).send({ status: "error", msg: "Invalid input" });

    input_uname = input_uname.trim();
    input_password = input_password.trim();

    try {
        await db.checkIfUserExists(input_uname).then(async (result) => {
            if (result)
                res.status(400).send({
                    status: "error",
                    msg: "Litey lite! This user already exists",
                });
            else {
                if (DEBUG)
                    console.log(`${req.ip} created new user: ${input_uname}`);
                await db
                    .addNewUserRecord(
                        input_uname,
                        await bcrypt.hash(input_password, process.env.SALT)
                    )
                    .then(async (result) => {
                        if (result) {
                            const _books = books.slice(0);
                            utils.shuffleArray(_books);
                            await db
                                .addNewUserBooks(
                                    input_uname,
                                    _books.slice(0, SAMPLE_BOOKS_LIMIT)
                                )
                                .then((result) =>
                                    result
                                        ? res.send({ goto: "/login" })
                                        : res.status(500).send({
                                              status: "error",
                                              msg: BACKEND_ERROR_MSG,
                                          })
                                );
                        } else
                            res.status(500).send({
                                status: "error",
                                msg: BACKEND_ERROR_MSG,
                            });
                    });
            }
        });
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.post("/api/login", async (req, res) => {
    let input_uname = req.query.username;
    let input_password = req.query.password;

    if (!input_uname || !input_password)
        return res
            .status(400)
            .send({ status: "error", msg: "All fields are mandatory" });

    if (!reUname.test(input_uname) || !rePass.test(input_password))
        return res.status(400).send({
            status: "error",
            msg: "Invalid credentials",
        });

    input_uname = input_uname.trim();
    input_password = input_password.trim();

    try {
        await db
            .checkUserPassword(
                input_uname,
                await bcrypt.hash(input_password, process.env.SALT)
            )
            .then(async (result) =>
                result
                    ? res.send({
                          token: utils.generateAccessToken(
                              result.username,
                              JWT_TOKEN_EXPIRY_SECONDS
                          ),
                          goto: "/",
                      })
                    : res.status(403).send({
                          status: "error",
                          msg: "Invalid credentials",
                      })
            );
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.get("/getBooks", utils.authCheck, (req, res) => {
    try {
        const db = new sqlite3.Database(
            `${process.env.DB_FOLDER}/${utils.getUsername(req)}.db`
        );
        db.serialize(() => {
            db.all(`SELECT * FROM BOOKS`, (err, rows) => {
                if (rows && rows.length !== 0)
                    res.send(
                        rows
                            ?.slice(0, MAX_VIEWABLE_BOOKS_LIMIT)
                            .map((row) => utils.removeUsernameFromData(row))
                    );
                else res.send([]);
            });
        });
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.get("/liteShare/:user/:liteId", utils.authCheck, async (req, res) => {
    return res.render("view", {
        maxInputLength: MAX_INPUT_LENGTH,
    });
});

app.get("/view/:user/:liteId", utils.authCheck, async (req, res) => {
    const input_uname = req.params.user;
    const liteId = req.params.liteId;

    if (!reUname.test(input_uname) || (liteId && liteId.length !== 10))
        return res.status(404).send([]);

    try {
        await db.checkIfUserExists(input_uname).then(async (result) => {
            if (!result) res.status(404).send([]);
            else {
                const db = new sqlite3.Database(
                    `${process.env.DB_FOLDER}/${input_uname}.db`
                );
                db.serialize(() => {
                    db.all(
                        `SELECT * FROM BOOKS WHERE liteId = ?`,
                        liteId,
                        (err, rows) => {
                            if (rows && rows.length !== 0)
                                res.send(
                                    rows
                                        ?.slice(0, SAMPLE_BOOKS_LIMIT + 2)
                                        .map((row) =>
                                            utils.removeUsernameFromData(row)
                                        )
                                );
                            else res.status(404).send([]);
                        }
                    );
                });
            }
        });
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.post("/api/create", utils.authCheck, async (req, res) => {
    try {
        const uname = utils.getUsername(req);
        if (uname === "admin")
            return utils.handleAdminLockedError(req, res, ADMIN_LOCKED_MSG);

        const data = req.body;

        const inputs = [
            data.title,
            data.author,
            data.pages,
            data.fav,
            data.read,
        ];
        let valid = true;
        for (const val in inputs)
            if (
                inputs[val] === undefined ||
                inputs[val] === null ||
                inputs[val] === NaN ||
                inputs[val] === ""
            ) {
                valid = false;
                break;
            }

        if (
            !valid ||
            !(typeof data.title === "string") ||
            !(typeof data.author === "string") ||
            !(typeof data.pages === "number") ||
            !(typeof data.imageLink === "string") ||
            !(typeof data.link === "string") ||
            !(typeof data.fav === "boolean") ||
            !(typeof data.read === "boolean") ||
            data.pages.toString().length > MAX_NUM_INPUT_LENGTH ||
            !(
                data.imageLink === "/assets/icons/bookshelf.svg" ||
                data.imageLink.startsWith(
                    "https://external-content.duckduckgo.com/iu/?u=https://covers.openlibrary.org/"
                )
            ) ||
            !(
                data.link === "" ||
                data.link.startsWith("https://openlibrary.org//works/")
            )
        )
            return res
                .status(400)
                .send({ status: "error", msg: "Invalid input" });

        if (
            data.title.length > MAX_INPUT_LENGTH ||
            data.author.length > MAX_INPUT_LENGTH ||
            data.imageLink.length > MAX_INPUT_LENGTH ||
            data.link.length > MAX_INPUT_LENGTH ||
            data.pages < 0 ||
            data.pages > 10000 * MAX_NUM_INPUT_LENGTH
        )
            return res
                .status(400)
                .send({ status: "error", msg: "Input ain't li(gh)te" });

        data.title = data.title.trim();
        data.author = utils.toTitleCase(data.author.trim());
        data.imageLink = data.imageLink.trim();
        data.link = data.link.trim();

        const username = utils.getUsername(req);

        await db
            .checkIfBookExists("create", username, data.title)
            .then((books) => {
                if (!books)
                    res.status(500).send({
                        status: "error",
                        msg: BACKEND_ERROR_MSG,
                    });
                else if (books.length >= MAX_BOOK_COUNT)
                    res.status(400).send({
                        status: "error",
                        msg: "You've got too many books! Need to stay li(gh)te here. Maybe try deleting some to free up space?",
                    });
                else {
                    if (books.length !== 0) {
                        const book = books.find((book) =>
                            book.title.includes(data.title)
                        );
                        if (book)
                            return res.status(400).send({
                                status: "error",
                                msg: "Book already exists in library",
                                book,
                            });
                    }

                    countBooks++;

                    const db = new sqlite3.Database(
                        `${process.env.DB_FOLDER}/${username}.db`
                    );
                    db.serialize(() => {
                        const liteId = nanoid.nanoid(
                            process.env.LENGTH_LITE_ID
                        );

                        const createStatement = db.prepare(
                            "INSERT INTO BOOKS VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
                        );
                        createStatement.run(
                            data.title,
                            data.author,
                            data.pages,
                            data.imageLink,
                            data.link,
                            data.fav,
                            data.read,
                            liteId
                        );
                        createStatement.finalize();

                        res.send({
                            status: "ok",
                            book: {
                                title: data.title,
                                author: data.author,
                                pages: data.pages,
                                imageLink: data.imageLink,
                                link: data.link,
                                fav: data.fav,
                                read: data.read,
                                liteId,
                            },
                        });
                    });
                }
            });
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.post("/api/update", utils.authCheck, async (req, res) => {
    try {
        const uname = utils.getUsername(req);
        if (uname === "admin")
            return utils.handleAdminLockedError(req, res, ADMIN_LOCKED_MSG);

        const data = req.body;

        if (
            data.title === undefined ||
            data.fav === undefined ||
            data.read === undefined ||
            !(typeof data.title === "string") ||
            !(typeof data.fav === "boolean") ||
            !(typeof data.read === "boolean") ||
            data.title === ""
        )
            return res
                .status(400)
                .send({ status: "error", msg: "Invalid input" });

        const username = utils.getUsername(req);

        await db
            .checkIfBookExists("update", username, data.title)
            .then((result) => {
                if (result === null)
                    res.status(500).send({
                        status: "error",
                        msg: BACKEND_ERROR_MSG,
                    });
                else if (!result)
                    res.status(404).send({
                        status: "error",
                        msg: "Book not found",
                    });
                else {
                    const db = new sqlite3.Database(
                        `${process.env.DB_FOLDER}/${username}.db`
                    );
                    db.serialize(() => {
                        const updateStatement = db.prepare(
                            "UPDATE BOOKS SET fav = ?, read = ? WHERE title = ?"
                        );
                        updateStatement.run(data.fav, data.read, data.title);
                        updateStatement.finalize();
                        res.send({
                            status: "ok",
                            book: {
                                ...result,
                                fav: data.fav ? "1" : "0",
                                read: data.read ? "1" : "0",
                            },
                        });
                    });
                }
            });
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.post("/api/delete", utils.authCheck, (req, res) => {
    try {
        const uname = utils.getUsername(req);
        const title = req.query.title;

        if (!(typeof title === "string") || title === "")
            return res
                .status(400)
                .send({ status: "error", msg: "Invalid input" });

        if (!utils.isSqlSafe(title))
            return res.status(404).send({
                status: "error",
                msg: "Book not found",
            });

        let db;
        if (uname === "admin")
            db = new sqlite3.Database(
                `${process.env.DB_FOLDER}/${uname}.db`,
                sqlite3.OPEN_READONLY
            );
        else db = new sqlite3.Database(`${process.env.DB_FOLDER}/${uname}.db`);
        db.serialize(() =>
            db.all(
                `SELECT title FROM BOOKS WHERE title = "${title}"`,
                async (err, rows) => {
                    if (!rows || rows.length === 0)
                        res.status(404).send({
                            status: "error",
                            msg: "Book not found",
                        });
                    else {
                        if (uname === "admin")
                            return res.send({
                                status: "ok",
                                book: rows[0],
                            });

                        const deleteStatement = db.prepare(
                            "DELETE FROM BOOKS WHERE title = ?"
                        );
                        deleteStatement.run(title);
                        deleteStatement.finalize();
                        res.send({ status: "ok", book: rows[0] });
                    }
                }
            )
        );
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.post("/report", utils.authCheck, async (req, res) => {
    const uname = utils.getUsername(req);
    if (uname === "admin")
        return utils.handleAdminLockedError(req, res, ADMIN_LOCKED_MSG);

    const data = req.body;

    const input_uname = data.user;
    const liteId = data.liteId;

    if (
        typeof input_uname !== "string" ||
        typeof liteId !== "string" ||
        !reUname.test(input_uname) ||
        (liteId && liteId.length !== 10)
    )
        return res.status(400).send({ status: "error", msg: "Invalid input" });

    if (input_uname === uname)
        return res.status(400).send({
            status: "error",
            msg: "How are we supposed to run lite if people go around reporting their own books?",
        });

    try {
        await db.checkIfUserExists(input_uname).then(async (result) => {
            !result
                ? res.status(404).send({
                      status: "error",
                      msg: "Invalid liteShare",
                  })
                : await db
                      .checkIfBookExists("report", input_uname, liteId)
                      .then(async (result) => {
                          if (result) {
                              if (DEBUG)
                                  console.log(
                                      `${SELF_HOST}/liteShare/${input_uname}/${liteId}`
                                  );

                              const socket = net.connect(
                                  {
                                      host: BOT_HOST,
                                      port: 1337,
                                  },
                                  () => {
                                      socket.write(
                                          `${SELF_HOST}?botToken=${process.env.BOT_ACCESS_TOKEN}|${SELF_HOST}/liteShare/${input_uname}/${liteId}`
                                      );
                                      socket.end();
                                  }
                              );

                              //   await setTimeout(
                              //       (() => socket.end(),
                              //       REPORT_BOT_KILL_TIMEOUT_SECONDS * 1000)
                              //   );

                              socket.on("error", (err) => {
                                  console.error("Socket Error", err.message);
                              });

                              res.send({
                                  status: "ok",
                                  msg: "Thank you for your report. We shall review it soon.",
                              });
                          } else
                              res.status(404).send({
                                  status: "error",
                                  msg: "Invalid liteShare",
                              });
                      });
        });
    } catch (e) {
        utils.handleError(req, res, e, BACKEND_ERROR_MSG);
    }
});

app.listen(PORT, () => console.log(`Serving on http://localhost:${PORT}/`));
