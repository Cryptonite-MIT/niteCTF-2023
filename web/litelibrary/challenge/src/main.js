const express = require("express");
const sqlite3 = require("sqlite3");
const helmet = require("helmet");
const morgan = require("morgan");
const rateLimit = require("express-rate-limit");

let PORT;
if (process.argv[2]) PORT = process.argv[2];
else {
    console.log("Exiting as listening port not provided");
    process.exit();
}

const DEFAULT_LIMIT = 7;
const SEARCH_LIMIT = 1;
const ASSETS_CACHE_TIME_SECONDS = 1800;

const BLACKLIST = ["delete", "update", "drop", "insert", "view", "sleep"];
const isSqlSafe = (input) => {
    let isSafe = true;
    BLACKLIST.forEach((word) => (input.includes(word) ? (isSafe = false) : {}));
    return isSafe;
};

const app = express();
const db = new sqlite3.Database("chalSqlite.db", sqlite3.OPEN_READONLY);

app.disable("x-powered-by");

// RATE LIMITED TO 0.5 RPS; resets every 5 minute
const limiter = rateLimit({
    windowMs: 0.5 * 60 * 1000 * 5,
    max: 300,
});
app.use("/api", limiter);

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

app.use(
    express.static("static", {
        maxAge: `${ASSETS_CACHE_TIME_SECONDS * 1000}`,
    })
);

app.get("/api/getBooks", (req, res) => {
    try {
        db.serialize(() =>
            db.all(`SELECT * FROM BOOKS`, (err, rows) => {
                if (rows !== undefined) res.send(rows?.slice(0, DEFAULT_LIMIT));
                else res.send([]);
            })
        );
    } catch (e) {
        console.log(`Error: ${e}`);
        res.send([]);
    }
});

app.get("/api/search", (req, res) => {
    if (!req.query.q) return res.send([]);
    const query = req.query.q.toLowerCase();

    if (isSqlSafe(query))
        try {
            db.serialize(() =>
                db.all(
                    `SELECT * FROM BOOKS WHERE title LIKE'%${query}%'`,
                    (err, rows) => {
                        if (!rows?.length) res.status(404).send([]);
                        else {
                            if (rows) res.send(rows?.slice(0, SEARCH_LIMIT));
                            else res.status(404).send([]);
                        }
                    }
                )
            );
        } catch (e) {
            console.log(`Error: ${e}`);
            res.send([]);
        }
    else return res.status(404).send([]);
});

app.get("/stats", (req, res) => {
    return res.send({ status: "ok", count: 50 });
});

app.listen(PORT, () => console.log(`Serving on http://localhost:${PORT}/`));
