#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import List

from tqdm import tqdm


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--takeout-root", type=str, default="Takeout")
    args = parser.parse_args()
    print(json.dumps(args.__dict__))  # , indent=2

    history_file = Path(args.takeout_root) / "マイ アクティビティ" / "Chrome" / "マイアクティビティ.json"
    with open(history_file) as f:
        history: List[dict] = json.load(f)

    # 1年間
    # {
    #     "header": "qiita.com",
    #     "products": ["Chrome"],
    #     "time": "2020-01-24T18:23:23.046Z",
    #     "title": "Ubuntuのディスク容量を見る - ...にアクセスしました",
    #     "titleUrl": "https://www.google....-LHe_SR3Q",
    # }
    infos = []
    google_search_url = "https://www.google.com/url?q="

    for page in tqdm(history):
        if "header" not in page:
            assert page["titleUrl"].startswith(google_search_url)
            continue

        if "titleUrl" not in page:
            assert page["title"] == "Chrome を使用しました"
            continue

        assert page["title"].rsplit(" ", 1)[-1] == "にアクセスしました"

        if page["header"] != page["titleUrl"][8:].split("/", 1)[0]:
            assert page["titleUrl"].startswith(google_search_url)
            page["titleUrl"] = page["titleUrl"][len(google_search_url):]

            if page["header"] != "Chrome":
                assert re.match(r"[\w-]+://([^:/]+)[:/$]", page["titleUrl"],)
                assert page["header"] == re.match(r"[\w-]+://([^:/]+)[:/$]", page["titleUrl"],)[1] or
                re.match(r"[\w-]+://([^:/]+)[:/$]", page["titleUrl"],)[1].endswith(page["header"])
                # {'www3.', 'www.', 'www2.', 'www33.', 'web.'}
        else:
            assert page["header"] != "Chrome"

        assert page["products"] == ["Chrome"]
        if page["titleUrl"].split(":", 1)[0] in ["http", "https"]:
            infos.append(
                {
                    "title": page["title"].rsplit(" ", 1)[0],
                    "url": page["titleUrl"],
                    "time": page["time"],
                    "domain": page["header"] if page["header"] != "Chrome" else re.match(r"[\w-]+://([^:/]+)[:/$]", page["titleUrl"],)[1],
                }
            )
        else:
            assert page["titleUrl"].split(":", 1)[0] in [
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
