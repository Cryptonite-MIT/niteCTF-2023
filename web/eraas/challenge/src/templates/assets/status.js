(async () => {
    await new Promise((r) => window.addEventListener("load", r));
    const btn = document.querySelector("#nudge");
    const respBox = document.querySelector("#nudgeResponse");
    try {
        btn.addEventListener("click", () =>
            fetch(
                `${window.origin}/nudge/${window.location.pathname.replace(
                    "/status/",
                    ""
                )}`
            )
                .then((r) => r.json())
                .then((r) => {
                    btn.textContent = "Done!";
                    btn.disabled = true;
                    if (r.status !== "ok")
                        respBox.textContent = `Error: ${r.message}`;
                })
        );
    } catch (e) {}
    try {
        if (!document.location.search.includes("token"))
            document.querySelector("#adminResponse").remove();
    } catch (e) {}
})();
