import requests
from bs4 import BeautifulSoup

from jinja2 import Template
from fastapi import FastAPI
from fastapi.responses import Response


app = FastAPI(title="api for my dynamic readme")


def get_scrobbles():
    r = requests.get("https://www.last.fm/user/arpy8")
    soup = BeautifulSoup(r.content)
    header_elements = soup.find_all('a', attrs={'href':'/user/arpy8/library'})

    return header_elements[1].text


@app.get("/")
def index() -> str:
    return "Hello!"

@app.get("/spotify_banner")
def spotify_banner() -> Response:
    SPOTIFY_SCROBBLES_TEMPLATE = """
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="310"
        height="90"
        viewBox="0 0 310 90"
        fill="none"
        role="img"
        aria-labelledby="descId"
        webcrx=""
        >
        <title id="titleId">Arpit's Spotify Stats</title>
        <desc id="descId">
            Total Scrobbles till now: {{ scrobbles }}
        </desc>
        <style>
        * {
        font: 18,'Segoe UI', Ubuntu, Sans-Serif;
        }
        .header {
        fill: #fff;
        font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
        animation: fadeInAnimation 0.8s ease-in-out forwards;
        }
        @supports (-moz-appearance: auto) {
        /* Selector detects Firefox */
        .header {
            font-size: 15.5px;
        }
        }

        .stat {
        font: 600 14px 'Segoe UI', Ubuntu, "Helvetica Neue", Sans-Serif; fill: #9f9f9f;
        fill: #9f9f9f;
        }
        @supports (-moz-appearance: auto) {
        /* Selector detects Firefox */
        .stat {
            font-size: 12px;
        }
        }
        .stagger {
        opacity: 0;
        animation: fadeInAnimation 0.3s ease-in-out forwards;
        }
    
        .not_bold {
        font-weight: 400;
        }
        .bold {
        font-weight: 700;
        }
        .icon {
        fill: #79ff97;
        display: block;
        }

        @keyframes scaleInAnimation {
        from {
            transform: translate(-5px, 5px) scale(0);
        }
        to {
            transform: translate(-5px, 5px) scale(1);
        }
        }
        @keyframes fadeInAnimation {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
        }
        </style>

        <rect
            data-testid="card-bg"
            x="0.5"
            y="0.5"
            rx="4.5"
            height="99%"
            stroke="#e4e2e2"
            width="308"
            fill="#151515"
            stroke-opacity="1"
        />

        <g data-testid="card-title" transform="translate(25, 35)">
            <g transform="translate(0, 0)">
            <text x="0" y="0" class="header" data-testid="header">
                Arpit's Spotify Stats
            </text>
            </g>
        </g>

        <g data-testid="main-card-body" transform="translate(0, 55)">
            <svg x="0" y="0">
            <g transform="translate(0, 0)">
                <g
                class="stagger"
                style="animation-delay: 450ms"
                transform="translate(25, 0)"
                >
                <svg
                data-testid="icon"
                class="icon"
                viewBox="0 0 16 16"
                version="1.1"
                width="16"
                height="16"
            >
                <path
                fill-rule="evenodd"
                d="M1.643 3.143L.427 1.927A.25.25 0 000 2.104V5.75c0 .138.112.25.25.25h3.646a.25.25 0 00.177-.427L2.715 4.215a6.5 6.5 0 11-1.18 4.458.75.75 0 10-1.493.154 8.001 8.001 0 101.6-5.684zM7.75 4a.75.75 0 01.75.75v2.992l2.028.812a.75.75 0 01-.557 1.392l-2.5-1A.75.75 0 017 8.25v-3.5A.75.75 0 017.75 4z"
                />
            </svg>

                <text class="stat bold" x="25" y="12.5">Total Scrobbles:</text>
                <text class="stat bold" x="219.01" y="12.5" data-testid="stars">
                    {{ scrobbles }}
                </text>
                </g>
            </g>
            </svg>
        </g>
        </svg>
    """
    template = Template(SPOTIFY_SCROBBLES_TEMPLATE)
    data = {
        "scrobbles": get_scrobbles()
    }
    
    return Response(content=template.render(data), media_type="image/svg+xml")