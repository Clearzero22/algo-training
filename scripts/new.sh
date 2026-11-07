#!/usr/bin/env bash
# 从模板生成一道题的解题文件,自动定位周目录和权威 slug。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TSV="$ROOT/data/problems.tsv"

usage() {
  cat <<'MSG'
用法: scripts/new.sh <语言> <题号> [--week N]

语言: python | java | cpp | go | typescript
例:
  scripts/new.sh python 15
  scripts/new.sh cpp 42
  scripts/new.sh java 51 --week 9
MSG
}

die() { printf 'error: %s\n' "$*" >&2; exit 1; }

[[ $# -ge 2 ]] || { usage; exit 1; }

lang="$1"
qid="$2"
shift 2

forced_week=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --week) forced_week="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "未知参数: $1" ;;
  esac
done

[[ "$qid" =~ ^[0-9]+$ ]] || die "题号必须是数字: $qid"

row="$(awk -F'\t' -v id="$qid" 'NR>1 && $2==id {print; exit}' "$TSV")"
[[ -n "$row" ]] || die "题号 $qid 不在 12 周计划里。查看 data/problems.tsv 确认。"

week="$(printf '%s' "$row" | cut -f1)"
slug="$(printf '%s' "$row" | cut -f3)"
title_cn="$(printf '%s' "$row" | cut -f4)"
difficulty="$(printf '%s' "$row" | cut -f6)"
[[ -n "$forced_week" ]] && week="$forced_week"

id4="$(printf '%04d' "$qid")"
weekdir="$(printf '%02d' "$week")"

case "$lang" in
  python)     fname="${id4}-${slug}.py" ;;
  java)       fname="Solution${id4}.java" ;;
  cpp)        fname="${id4}_${slug}.cpp" ;;
  go)         fname="${id4}_${slug}.go" ;;
  typescript) fname="${id4}-${slug}.ts" ;;
  *) die "不支持的语言: $lang(可用: python java cpp go typescript)" ;;
esac

tpl="$ROOT/solutions/$lang/_template.${fname##*.}"
[[ -f "$tpl" ]] || die "模板不存在: $tpl"

dir="$ROOT/solutions/$lang/week-$weekdir"
target="$dir/$fname"
mkdir -p "$dir"

if [[ -e "$target" ]]; then
  die "文件已存在,未覆盖: $target"
fi

sed "s|{题号} {题名}|${qid} ${title_cn}|" "$tpl" > "$target"

printf '已创建 %s\n' "${target#"$ROOT"/}"
printf '  第 %s 周 · %s · %s\n' "$week" "$title_cn" "$difficulty"
