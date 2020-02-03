#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
from typing import List
from tqdm import tqdm
from time import sleep
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--takeout-root", type=str, default="Takeout")
    args = parser.parse_args()
    print(json.dumps(args.__dict__))  # , indent=2

    history_file = Path(args.takeout_root) / "マイ アクティビティ" / "YouTube" / "マイアクティビティ.json"
    with open(history_file) as f:
        history: List[dict] = json.load(f)

    # 全記録
    # {
    #     "header": "YouTube",
    #     "products": ["YouTube"],
    #     "subtitles": [
    #         {
    #             "name": "楽器・音楽の総合チャンネル！アルファノートTV",
    #             "url": "https://www.youtube...-pyG_uoeg",
    #         }
    #     ],
    #     "time": "2020-01-24T17:43:25.036Z",
    #     "title": "メトロノーム練習用テンポ60 を視聴しました",
    #     "titleUrl": "https://www.youtube...ADzsPg4Jc",
    # }
    infos = []
    untitles = []

    for page in tqdm(history):
        if "titleUrl" not in page:
            if page["title"].rsplit(" ", 1)[-1] == "のストーリーを視聴しました":
                pass
            elif page["title"] == "削除済みの動画を視聴しました":
                pass
            elif page["title"] == "YouTube Music にアクセスしました":
                pass
            else:
                assert False
            continue
        if "subtitles" not in page:
            if page["title"].rsplit(" ", 1)[-1] == "」を検索しました":
                pass
            else:
                assert page["title"] == f"{page['titleUrl']} を視聴しました"
                untitles.append({"time": page["time"], "title_url": page["titleUrl"]})
            continue

        assert page["header"] in ["YouTube", "YouTube Music"]
        assert page["products"] == ["YouTube"]
        assert len(page["subtitles"]) == 1

        infos.append(
            {
                "title": page["title"],
                "title_url": page["titleUrl"],
                "time": page["time"],
                "channel": page["subtitles"][0]["name"],
                "channel_url": page["subtitles"][0]["url"],
            }
        )

    print(f"infos: {len(infos)}")
    print(f"history: {len(history)}")


if __name__ == "__main__":
    main()
