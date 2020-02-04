#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List

from tqdm import tqdm


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--takeout-root", type=str, default="Takeout")
    args = parser.parse_args()
    print(json.dumps(args.__dict__))  # , indent=2

    history_file = Path(args.takeout_root) / "Chrome" / "BrowserHistory.json"
    with open(history_file) as f:
        history = json.load(f)
        assert len(history) == 1

    history: List[dict] = history["Browser History"]
    # 1年間
    # {
    #     "client_id": "M7HN9wdfkhemOtXt4MoTOg==",
    #     "favicon_url": "https://www.google....vicon.ico",
    #     "page_transition": "LINK",
    #     "time_usec": 1579891134036550,
    #     "title": "Google データ エクスポート",
    #     "url": "https://takeout.google.com/",
    # }
    infos = []

    for page in tqdm(history):
        if page["url"].split(":", 1)[0] in ["http", "https"]:
            assert page["page_transition"] in [
                "LINK",
                "FORM_SUBMIT",
                "GENERATED",
                "AUTO_BOOKMARK",
                "RELOAD",
                "AUTO_TOPLEVEL",
                "TYPED",
                "KEYWORD",
            ]
            assert re.match(r"[\w-]+://([^:/]+)[:/$]", page["url"])
            infos.append(
                {
                    "client": page["client_id"],
                    "title": page["title"],
                    "url": page["url"],
                    "time": str(datetime.fromtimestamp(page["time_usec"] / 1000000)),
                    "domain": re.match(r"[\w-]+://([^:/]+)[:/$]", page["url"])[1],
                }
            )
        else:
            assert page["url"].split(":", 1)[0] in [
                "chrome",
                "chrome-extension",
                "devtools",
                "chrome-devtools",
                "data",
                "blob",
                "ws",
                "view-source",
                "about",
                "chrome-native",
                "chrome-distiller",
                "chrome-search",
                "file",
            ]

    print(f"infos: {len(infos)}")
    print(f"history: {len(history)}")


if __name__ == "__main__":
    main()
