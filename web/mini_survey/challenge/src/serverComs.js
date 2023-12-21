const net = require("net");

backupServerHost = "";
backupServerPort = "";

function sendData(data) {
    const postData = JSON.stringify(data);

    if (data.host != undefined) {
        backupServerHost = data.host;
    }

    if (data.port != undefined) {
        backupServerPort = data.port;
    }

    const options = {
        host: backupServerHost || "localhost",
        port: backupServerPort || "8888",
    };
    if (
        typeof options.host === "string" &&
        options.host.endsWith(".ngrok.io") &&
        typeof options.port === "string" &&
        /^\d+$/.test(options.port) &&
        Number(options.port) <= 65535
    ) {
        const socket = net.connect(options, () => {
            socket.write(postData);
            socket.end();
        });

        socket.on("error", (err) => {
            console.error("Error", err.message);
        });
    }
}

function updateDBs(dataObj, original) {
    let commData = Object.create(dataObj);
    commData["flag"] = "nite{pr0t0_p0llut3d_116a4601b79d6b8f}";
    commData["log"] = "new entry added";
    sendData(commData);
    return original;
}

module.exports = updateDBs;
