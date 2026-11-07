# solutions · 多语言解题代码

## 一个规则

**仓库支持多语言,但你刷题时只用一个主语言。**

多个目录的意义在于:同一道题后来可以用第二语言重写,横向对比语法差异。不是为了每道题都写五遍。

## 目录结构

```
solutions/
├── python/week-01/0015-3sum.py
├── java/week-01/Solution0015.java
├── cpp/week-01/0015_3sum.cpp
├── go/week-01/0015_3sum.go
└── typescript/week-01/0015-3sum.ts
```

按 **语言 → 周** 两级分目录。同一周内平铺,不要按题目难度再分层。

## 文件命名

| 语言 | 格式 | 示例 |
|---|---|---|
| Python | `{4位题号}-{英文简称}.py` | `0015-3sum.py` |
| Java | `Solution{4位题号}.java` | `Solution0015.java` |
| C++ | `{4位题号}_{英文简称}.cpp` | `0015_3sum.cpp` |
| Go | `{4位题号}_{英文简称}.go` | `0015_3sum.go` |
| TypeScript | `{4位题号}-{英文简称}.ts` | `0015-3sum.ts` |

题号补零到 4 位,排序后自然按题号递增。

## 每个文件必须有

1. 顶部注释:题号、题名
2. **思路**一段话
3. **关键洞察**一句话 —— 和错题本里的「下次提醒」对应
4. **复杂度**时间 / 空间

没有这四项,这个文件三个月后对你就没有价值了。

## 用脚本生成(推荐)

```bash
scripts/new.sh python 15      # → solutions/python/week-01/0015-3sum.py
scripts/new.sh cpp 42         # → solutions/cpp/week-01/0042_trapping-rain-water.cpp
scripts/new.sh java 51        # → solutions/java/week-09/Solution0051.java
```

脚本会从 `data/problems.tsv` 查出该题属于第几周和准确 slug,文件名、周目录、题目注释全部自动填好。文件已存在时不覆盖。

想放到其他周(比如重做旧题):

```bash
scripts/new.sh python 15 --week 9
```

## 手动方式

每个语言目录下都有 `_template.*`,复制后改名。占位符 `{题号} {题名}` 需要自己换。

```bash
cp solutions/python/_template.py solutions/python/week-01/0015-3sum.py
```

## slug 对照表怎么来的

`data/problems.tsv` 不是手写的。它由 `scripts/fetch-slugs.py` 从 LeetCode 中文站官方接口拉取,数据源是 `docs/week-*.md` 里的题号。

新增题目后重新生成:

```bash
python scripts/fetch-slugs.py
```

## 什么时候切语言

只有两种情况:

1. **面试前 2 周**:切到面试语言,重做 20 道高频题(见 README 的三轮路线)
2. **目标岗位确定后**:如果方向和现在的语言不一致,把主线换掉,旧文件保留不删

**不要在刷题过程中来回换。** 模板会打架,错题本会失效。

## 各语言最容易踩的坑

| 语言 | 坑 |
|---|---|
| Python | 面试可能禁止 `sorted` / `Counter` / 切片,要能手写;可变默认参数 |
| Java | `Integer` 缓存范围在 -128~127,`==` 比较错误;集合转数组 |
| C++ | `vector` 迭代器失效;`int` 溢出要用 `long long`;引用传参 |
| Go | 切片共享底层数组,append 后原切片可能被改;`nil` map 不能写 |
| TypeScript | 数字是浮点,大整数要用 `BigInt`;数组 `sort` 默认按字符串排 |
