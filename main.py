#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from tqdm import tqdm

from Chrome import load_data as chrome_load
from MyActivity_Chrome import load_data as my_activity_chrome_load
from MyActivity_YouTube import load_data as my_activity_youtube_load
from YouTube import load_data as youtube_load


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--takeout-root", type=str, default="Takeout")
    args = parser.parse_args()
    print(json.dumps(args.__dict__))  # , indent=2

    takeout_root = Path(args.takeout_root)

    chrome_load(takeout_root / "Chrome" / "BrowserHistory.json")
    my_activity_chrome_load(takeout_root / "マイ アクティビティ" / "Chrome" / "マイアクティビティ.json")
    youtube_load(takeout_root / "YouTube" / "履歴" / "watch-history.json")
    my_activity_youtube_load(takeout_root / "マイ アクティビティ" / "YouTube" / "マイアクティビティ.json")


if __name__ == "__main__":
    main()
