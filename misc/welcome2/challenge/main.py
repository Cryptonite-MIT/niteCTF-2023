from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


URL_HEADER = "https://nitectf.live/"
URL_FOOTER = "https://cryptonite.live/"
TITLE = "niteCTF 2023 💎 is now live!"

FLAGS = {
    "facebookexternalhit": "bml0ZXtsMW5rXw",
    "WhatsApp": "cHIzdjEzdzVfZnR3Xzcx",
    "TwitterBot": "NTBfdGgzeV81NXJmfQ",
}

app = FastAPI()
app.mount("/assets", StaticFiles(directory="static/assets", html=True))
templates = Jinja2Templates(directory="static")


@app.get("/")
def response(request: Request):
    ua = request.headers.get("user-agent")
    for key in FLAGS.keys():
        if key in ua:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "title": "{} {}".format(TITLE, FLAGS[key]),
                    "url_header": URL_HEADER,
                    "url_footer": URL_FOOTER,
                },
            )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": TITLE,
            "url_header": URL_HEADER,
            "url_footer": URL_FOOTER,
        },
    )


# red herrings
@app.get("/robots.txt")
def response(request: Request):
    return templates.TemplateResponse("robots.txt", {"request": request})


@app.get("/backend_config")
def response(request: Request):
    response = templates.TemplateResponse("backend_config.html", {"request": request})
    response.set_cookie(
        key="session",
        value='{"type":"user","last_page":"backend_config","secretv3":"d131dd02c5e6eec4693d9a0698aff95c"}',
        httponly=True,
    )
    return response
