const jwt = require("jsonwebtoken");

const generateAccessToken = (data, expiryTimeInSeconds = 60) =>
    jwt.sign({ data }, process.env.JWT_SECRET, {
        expiresIn: `${expiryTimeInSeconds}s`,
    });

const authCheck = (req, res, next) => {
    let ip = req.connection.remoteAddress;
    ip = ip.split("ff:")[1]?.split(".")[0];

    // direct admin entry to bot, only when visiting from localhost
    if (req.query.botToken === process.env.BOT_ACCESS_TOKEN && ip === "10") {
        const expireInSeconds = 20;
        const token = generateAccessToken("admin", expireInSeconds);
        const expires = new Date();
        expires.setTime(expires.getTime() + expireInSeconds * 1000);

        res.cookie("token", token, { expires });
        return res.redirect("/");
    }

    const token = req.cookies.token;
    if (token) {
        if (
            jwt.verify(token, process.env.JWT_SECRET, (err, data) => {
                if (req.url === "/login" || req.url === "/register")
                    if (err) next();
                    else res.redirect("/");
                else if (!err) {
                    // limit admin account access local
                    if (data?.data === "admin" && ip !== "10") return true;

                    next();
                } else return true;
            })
        ) {
            // delete token client side if it is invalid
            res.cookie("token", "", { expires: new Date(0) });
            return res.redirect("/login");
        }
    } else if (req.url === "/login" || req.url === "/register") return next();
    else return res.redirect("/login");
};

const getUsername = (req) => {
    return jwt.verify(req.cookies.token, process.env.JWT_SECRET, (err, data) =>
        err ? null : data?.data
    );
};

const shuffleArray = (array) => {
    let currentIndex = array.length,
        randomIndex;
    while (currentIndex > 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex],
            array[currentIndex],
        ];
    }

    return array;
};

const removeUsernameFromData = (book) => {
    delete book.username;
    return book;
};

const toTitleCase = (str) => {
    try {
        return str
            .split(" ")
            .map((w) => {
                if (w === "") return;
                return w[0].toUpperCase() + w.substring(1).toLowerCase();
            })
            .join(" ");
    } catch (e) {
        return str;
    }
};

const handleError = (req, res, error, msg) => {
    console.log(`# ERROR at ${req.url}: ${error}`);
    return res.status(500).send({
        status: "error",
        msg,
    });
};

const handleAdminLockedError = (req, res, msg) => {
    // console.log(`# Stopped admit edit at ${req.url}`);
    return res.status(400).send({
        status: "error",
        msg,
    });
};

const BLACKLIST = ["delete", "update", "drop", "insert", "view", "sleep"];
const isSqlSafe = (input) => {
    let isSafe = true;
    BLACKLIST.forEach((word) =>
        input.toLowerCase().includes(word) ? (isSafe = false) : {}
    );
    return isSafe;
};

module.exports = {
    generateAccessToken,
    authCheck,
    getUsername,
    shuffleArray,
    removeUsernameFromData,
    toTitleCase,
    handleError,
    handleAdminLockedError,
    isSqlSafe,
};
