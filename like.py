import io
import sys
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class HZAULiker:
    def __init__(self, uid="0", homepageid="0"):
        self.base = "https://faculty.hzau.edu.cn"
        self.praise_url = f"{self.base}/system/resource/tsites/praise.jsp"
        self.uid = uid
        self.homepageid = homepageid
        self.session = requests.Session()

    def _make_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
            "Origin": self.base,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    def get_count(self):
        data = {
            "uid": self.uid,
            "homepageid": self.homepageid,
            "apptype": "index",
            "contentid": "0",
            "pdtype": "0",
            "basenum": "0",
            "ac": "getPraise",
        }
        r = self.session.post(
            self.praise_url, data=data, headers=self._make_headers(), timeout=15
        )
        return r.json().get("praise", 0)

    def like(self):
        data = {
            "uid": self.uid,
            "homepageid": self.homepageid,
            "apptype": "index",
            "contentid": "0",
            "pdtype": "0",
            "ac": "updatePraise",
        }
        r = self.session.post(
            self.praise_url, data=data, headers=self._make_headers(), timeout=15
        )
        return r.status_code == 200

    def batch_like(self, count, threads=5):
        before = self.get_count()
        print(f"当前点赞数: {before}")

        ok = 0
        with ThreadPoolExecutor(max_workers=threads) as pool:
            futures = [pool.submit(self.like) for _ in range(count)]
            for i, f in enumerate(as_completed(futures), 1):
                if f.result():
                    ok += 1
                if i % 10 == 0 or i == count:
                    print(f"进度: {i}/{count}, 成功: {ok}")

        after = self.get_count()
        net = after - before
        print(f"完成! 当前点赞数: {after}, 净增: {net}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="华中农大教师主页刷赞脚本")
    parser.add_argument("-n", type=int, default=100, help="点赞次数 (默认: 100)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="并发线程数 (默认: 5)")
    parser.add_argument("--uid", type=str, default="0", help="教师UID")
    parser.add_argument("--homepageid", type=str, default="0", help="主页ID")
    args = parser.parse_args()

    liker = HZAULiker(uid=args.uid, homepageid=args.homepageid)
    liker.batch_like(args.n, args.threads)
