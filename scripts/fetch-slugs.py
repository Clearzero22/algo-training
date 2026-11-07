#!/usr/bin/env python3
"""从 docs/week-XX.md 解析题号,再向 LeetCode 中文站查权威 slug,生成 data/problems.tsv。

单一数据源是 docs/ 下的周清单,不在这里硬编码题号。
需要更新时重跑即可: python scripts/fetch-slugs.py
"""
import glob
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUERY = """
query q($limit: Int, $skip: Int) {
  problemsetQuestionList(categorySlug: "", limit: $limit, skip: $skip, filters: {}) {
    total
    questions { frontendQuestionId titleSlug title titleCn difficulty }
  }
}
"""
URL = "https://leetcode.cn/graphql/"


def post(payload):
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={
            "content-type": "application/json",
            "referer": "https://leetcode.cn/problemset/",
            "user-agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fetch_all():
    out, skip, total = [], 0, None
    while total is None or skip < total:
        data = post({"query": QUERY, "variables": {"limit": 100, "skip": skip}})
        block = data["data"]["problemsetQuestionList"]
        total = block["total"]
        out.extend(block["questions"])
        skip += 100
        print(f"  已拉取 {min(skip, total)}/{total}", file=sys.stderr)
        time.sleep(0.3)
    return out


def parse_plan():
    plan = []
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "week-*.md"))):
        week = int(re.search(r"week-(\d+)", path).group(1))
        with open(path, encoding="utf-8") as f:
            for qid in re.findall(r"^- \[[ x]\] \*\*(\d+)\*\*", f.read(), re.M):
                plan.append((week, qid))
    return plan


def main():
    plan = parse_plan()
    ids = {qid for _, qid in plan}
    print(f"计划内题目 {len(ids)} 道,开始查询 LeetCode...", file=sys.stderr)
    allq = fetch_all()

    index = {}
    for q in allq:
        index[q["frontendQuestionId"]] = q

    missing = sorted(ids - index.keys(), key=int)
    if missing:
        print(f"警告:以下题号未在 LeetCode 找到: {missing}", file=sys.stderr)

    out = os.path.join(ROOT, "data", "problems.tsv")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("week\tid\tslug\ttitle_cn\ttitle\tdifficulty\n")
        for week, qid in plan:
            q = index.get(qid)
            if not q:
                continue
            f.write(
                f"{week}\t{qid}\t{q['titleSlug']}\t{q['titleCn']}\t"
                f"{q['title']}\t{q['difficulty']}\n"
            )
    print(f"已写入 {out}({len(plan)} 行)", file=sys.stderr)


if __name__ == "__main__":
    main()
