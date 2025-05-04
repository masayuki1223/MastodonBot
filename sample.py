# ファイル名を定義
QUOTES_FILE = "sample.txt"
PICKLE_FILE = "sample.pkl"
ENV_FILE = ".env_sample"

from dotenv import load_dotenv
import os
from mastodon import Mastodon
import random
import pickle

def save_order_to_pickle(order):
    """並び順をpickleファイルに保存"""
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(order, f)

def load_order_from_pickle():
    """pickleファイルから並び順を読み込む"""
    try:
        with open(PICKLE_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def load_quotes(file_path):
    """
    テキストファイルを読み込み:
    - 先頭が#の行を無視
    - 空行を無視
    - \nを実際の改行に変換
    """
    quotes = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()  # 行の前後の空白を削除
            if line.startswith("#") or not line:
                # コメント行や空行をスキップ
                continue
            # \nを実際の改行に変換してリストに追加
            quotes.append(line.replace("\\n", "\n"))
    return quotes

def serect_quote():
    strings = load_quotes(QUOTES_FILE)

    # 名言に対応する番号（インデックス）
    word_numbers = list(range(len(strings)))

    # pickleから現在の順番を読み込む
    current_order = load_order_from_pickle()

    if current_order:
        # 現在の順番が存在する場合、次の番号に対応する名言を出力
        next_word_index = current_order.pop(0)

        # 残りの順番をpickleに保存
        if current_order:
            save_order_to_pickle(current_order)
        else:
            # 全名言を表示したので新しいランダム順番を生成
            new_order = random.sample(word_numbers, len(strings))
            save_order_to_pickle(new_order)
        return(strings[next_word_index])
    else:
        # 初回の場合、新しいランダム順番を生成し、最初の名言を出力
        new_order = random.sample(word_numbers, len(strings))
        first_word_index = new_order.pop(0)
        save_order_to_pickle(new_order)
        return(strings[first_word_index])

def post_quote():
    load_dotenv(ENV_FILE)  # ファイル名を指定する場合
    # 初期化
    api = Mastodon(
        api_base_url = os.getenv("MASTODON_BASE_URL"),
        client_id = os.getenv("MASTODON_CLIENT_ID"),
        client_secret = os.getenv("MASTODON_CLIENT_SECRET"),
        access_token = os.getenv("MASTODON_ACCESS_TOKEN"),
    )

    string = serect_quote()
    api.toot(string)

def print_quote():
    string = serect_quote()
    print(string)

if __name__ == "__main__":  # ターミナルから実行された場合のみ動作
    post_quote()
