#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from tqdm import tqdm


def load_data(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path) as f:
        raw_data: List[dict] = json.load(f)
    # 1年間
    # {
    #     "header": "YouTube",
    #     "products": ["YouTube"],
    #     "subtitles": [{"name": "コカ・コーラ", "url": "https://www.youtube...bDY6Gi3WQ"}],
    #     "time": "2020-01-24T17:45:17.963Z",
    #     "title": "【アクエリアス】 TVCM 『見えない...F を視聴しました",
    #     "titleUrl": "https://www.youtube...w1ji5_CXI",
    # }
    history = []
    non_public = []  # 非公開動画

    for page in tqdm(raw_data):
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
            assert page["title"] == f"{page['titleUrl']} を視聴しました"
            non_public.append({"time": page["time"], "title_url": page["titleUrl"]})
            continue

        assert page["header"] in ["YouTube", "YouTube Music"]
        assert page["products"] == ["YouTube"]
        assert len(page["subtitles"]) == 1

        history.append(
            {
                "title": page["title"][:-8],
                "title_url": page["titleUrl"],
                "time": page["time"],
                "channel": page["subtitles"][0]["name"],
                "channel_url": page["subtitles"][0]["url"],
            }
        )

    print(f"{len(history)}[{len(history) / len(raw_data):.1%}]のデータが読み込まれました")
    return history


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--takeout-root", type=str, default="Takeout")
    args = parser.parse_args()
    print(json.dumps(args.__dict__))  # , indent=2

    history_file = Path(args.takeout_root) / "YouTube" / "履歴" / "watch-history.json"

    history = load_data(history_file)


if __name__ == "__main__":
    main()
