const dotenv = require("dotenv");
const fs = require("fs");

const db = require("./utilsDb.js");
const data = require("./startingData.json");

dotenv.config();

fs.rmSync(process.env.DB_FOLDER, { recursive: true, force: true });
fs.mkdirSync(process.env.DB_FOLDER);

(async function () {
    await db.initUsersDb();
    data["users"].forEach(
        async (user) => await db.addNewUserRecord(user.username, user.hash)
    );
    console.log("DB: Users ready");

    await db.addNewUserBooks("admin", data["users"][0]["books"]);
    console.log("DB: Books ready");
})();
