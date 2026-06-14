#!/usr/bin/env python3
"""Local mechanical workflows for the fuxi knowledge base."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "fuxi.config.json"
FRONTMATTER_BOUNDARY = "---"
LIST_FIELDS = {"tags", "keywords", "related", "concepts"}
SECTION_PATTERN = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9._+-]*|[\u4e00-\u9fff]{2,}")
STOPWORDS = {
    "一个",
    "一种",
    "以及",
    "使用",
    "可以",
    "进行",
    "相关",
    "通过",
    "需要",
    "这个",
    "这些",
    "目前",
    "其中",
    "我的",
    "视频文档",
}


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def clean_scalar(value: str) -> str:
    return value.strip().strip("\"'")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse the small YAML subset used by fuxi without external packages."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        return {}, text

    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == FRONTMATTER_BOUNDARY
        )
    except StopIteration:
        return {}, text

    data: dict[str, Any] = {}
    current_list: str | None = None
    review: dict[str, Any] = {}
    in_review = False
    review_list: str | None = None

    for raw_line in lines[1:end]:
        if not raw_line.strip():
            continue

        indent = len(raw_line) - len(raw_line.lstrip())
        line = raw_line.strip()

        if line == "review:":
            in_review = True
            current_list = None
            continue

        if indent == 0:
            in_review = False
            review_list = None

        if line.startswith("- "):
            item = clean_scalar(line[2:])
            target = review if in_review else data
            key = review_list if in_review else current_list
            if key:
                target.setdefault(key, []).append(item)
            continue

        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = clean_scalar(raw_value)
        target = review if in_review else data

        if value == "[]":
            target[key] = []
            review_list = None
            current_list = None
            continue

        if not value:
            target[key] = [] if key in LIST_FIELDS else ""
            if key in LIST_FIELDS:
                if in_review:
                    review_list = key
                else:
                    current_list = key
            else:
                review_list = None
                current_list = None
            continue

        target[key] = value
        if in_review:
            review_list = None
        else:
            current_list = None

    if review:
        data["review"] = review
    return data, "\n".join(lines[end + 1 :]).lstrip()


def yaml_items(values: Iterable[str], indent: int = 0) -> list[str]:
    prefix = " " * indent
    items = [str(value).strip() for value in values if str(value).strip()]
    return [f"{prefix}- {item}" for item in items]


def append_list_field(lines: list[str], key: str, values: Iterable[str], indent: int = 0) -> None:
    prefix = " " * indent
    items = [str(value).strip() for value in values if str(value).strip()]
    if not items:
        lines.append(f"{prefix}{key}: []")
        return
    lines.append(f"{prefix}{key}:")
    lines.extend(yaml_items(items, indent + 2))


def render_frontmatter(metadata: dict[str, Any]) -> str:
    review = metadata.get("review") or {}
    lines = [
        FRONTMATTER_BOUNDARY,
        f"title: {metadata.get('title', '')}",
        f"type: {metadata.get('type', 'source_note')}",
        f"source: {metadata.get('source', '')}",
        f"created: {metadata.get('created', '')}",
        f"updated: {metadata.get('updated', '')}",
    ]
    append_list_field(lines, "tags", metadata.get("tags", []))
    append_list_field(lines, "keywords", metadata.get("keywords", []))
    append_list_field(lines, "related", metadata.get("related", []))
    lines.extend(
        [
            "review:",
            f"  status: {review.get('status', 'candidate')}",
        ]
    )
    append_list_field(lines, "concepts", review.get("concepts", []), 2)
    lines.extend(
        [
            f"  last_reviewed: {review.get('last_reviewed', '')}",
            f"  next_review: {review.get('next_review', '')}",
            FRONTMATTER_BOUNDARY,
        ]
    )
    return "\n".join(lines)


def write_note(path: Path, metadata: dict[str, Any], body: str) -> None:
    path.write_text(
        f"{render_frontmatter(metadata)}\n\n{body.rstrip()}\n",
        encoding="utf-8",
    )


def safe_slug(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value.strip())
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-_.")
    return value[:80] or "untitled"


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()[:12]


def unique_destination(directory: Path, filename: str, digest: str) -> Path:
    candidate = directory / filename
    if not candidate.exists():
        return candidate
    if candidate.is_file() and file_digest(candidate) == digest:
        return candidate
    stem = candidate.stem
    return directory / f"{stem}-{digest}{candidate.suffix}"


def first_meaningful_lines(text: str, limit: int = 3) -> list[str]:
    result: list[str] = []
    in_frontmatter = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == FRONTMATTER_BOUNDARY and not result:
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not stripped or stripped.startswith("#"):
            continue
        result.append(stripped)
        if len(result) >= limit:
            break
    return result


def section_text(body: str, heading: str) -> str:
    """Return one top-level Markdown section without its heading."""
    matches = list(SECTION_PATTERN.finditer(body))
    for index, match in enumerate(matches):
        if match.group(1).strip() != heading:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        return body[start:end].strip()
    return ""


def compact_text(text: str, limit: int = 80) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    value = re.sub(r"^[-*>#\d.\s]+", "", value)
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def note_summary(body: str) -> str:
    summary = section_text(body, "摘要")
    candidates = first_meaningful_lines(summary or body, limit=1)
    return compact_text(candidates[0], 80) if candidates else ""


def title_tokens(title: str) -> set[str]:
    tokens: set[str] = set()
    for token in TOKEN_PATTERN.findall(title):
        normalized = token.casefold()
        if normalized not in STOPWORDS:
            tokens.add(normalized)
    return tokens


def parse_iso_date(value: Any) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def markdown_escape(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def build_note_body(raw_text: str) -> str:
    preview = "\n\n".join(first_meaningful_lines(raw_text))
    if not preview:
        preview = "等待 AI 阅读原文后补充。"
    return f"""# 摘要

{preview}

# 核心观点

等待 AI 阅读原文后补充。

# 我的理解

等待 AI 结合个人目标补充。

# 可复用方法

等待 AI 提炼。

# 项目关联

等待 AI 判断。

# 需要复习的知识点

等待 AI 识别。
"""


def iter_source_files(source: Path, config: dict[str, Any]) -> Iterable[Path]:
    supported = {suffix.lower() for suffix in config["supported_extensions"]}
    ignored = set(config["ignored_directories"])

    if source.is_file():
        if source.suffix.lower() in supported:
            yield source
        return

    for path in source.rglob("*"):
        if any(part in ignored for part in path.relative_to(source).parts[:-1]):
            continue
        if path.is_file() and path.suffix.lower() in supported:
            yield path


def ingest_file(source: Path) -> tuple[Path, Path]:
    raw_dir = ROOT / "raw"
    notes_dir = ROOT / "notes"
    digest = file_digest(source)
    day = date.today().isoformat()
    raw_name = f"{day}-{safe_slug(source.stem)}{source.suffix.lower()}"
    raw_path = unique_destination(raw_dir, raw_name, digest)

    if not raw_path.exists():
        shutil.copy2(source, raw_path)

    raw_text = raw_path.read_text(encoding="utf-8", errors="replace")
    note_path = notes_dir / f"{day}-{safe_slug(source.stem)}-{digest}.md"
    if note_path.exists():
        return raw_path, note_path

    metadata = {
        "title": source.stem,
        "type": "source_note",
        "source": raw_path.relative_to(ROOT).as_posix(),
        "created": day,
        "updated": day,
        "tags": [],
        "keywords": [],
        "related": [],
        "review": {
            "status": "candidate",
            "concepts": [],
            "last_reviewed": "",
            "next_review": "",
        },
    }
    write_note(note_path, metadata, build_note_body(raw_text))
    return raw_path, note_path


def load_notes() -> list[tuple[Path, dict[str, Any], str]]:
    notes = []
    for path in sorted((ROOT / "notes").glob("*.md")):
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if metadata:
            notes.append((path, metadata, body))
    return notes


def build_index() -> Path:
    rows = []
    for path, metadata, body in load_notes():
        review = metadata.get("review") or {}
        tags = ", ".join(metadata.get("tags") or [])
        concepts = ", ".join(review.get("concepts") or [])
        topics = ", ".join(sorted(set(metadata.get("tags") or [])))
        rows.append(
            "| {title} | [{file}](notes/{file}) | {kind} | {tags} | {summary} | {topics} | {concepts} | {status} | {created} |".format(
                title=markdown_escape(metadata.get("title", "")),
                file=path.name,
                kind=markdown_escape(metadata.get("type", "")),
                tags=markdown_escape(tags),
                summary=markdown_escape(note_summary(body)),
                topics=markdown_escape(topics),
                concepts=markdown_escape(concepts),
                status=markdown_escape(review.get("status", "")),
                created=markdown_escape(metadata.get("created", "")),
            )
        )

    wiki_links = [
        f"- [{path.stem}](wiki/{path.name})"
        for path in sorted((ROOT / "wiki").glob("*.md"))
    ]
    content = [
        "# fuxi 知识库索引",
        "",
        f"> 最近更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 标题 | 文件 | 类型 | 标签 | 摘要 | 相关主题 | 复习知识点 | 复习状态 | 创建时间 |",
        "|---|---|---|---|---|---|---|---|---|",
        *rows,
        "",
        "## 主题页",
        "",
        *(wiki_links or ["当前没有主题页。"]),
        "",
    ]
    index_path = ROOT / "INDEX.md"
    index_path.write_text("\n".join(content), encoding="utf-8")
    return index_path


def relation_score(
    left: dict[str, Any],
    right: dict[str, Any],
    config: dict[str, Any],
) -> int:
    left_tags = set(left.get("tags") or [])
    right_tags = set(right.get("tags") or [])
    left_keywords = set(left.get("keywords") or [])
    right_keywords = set(right.get("keywords") or [])
    shared_title_tokens = title_tokens(str(left.get("title", ""))) & title_tokens(
        str(right.get("title", ""))
    )
    return (
        len(left_tags & right_tags) * int(config["tag_score"])
        + len(left_keywords & right_keywords) * int(config["keyword_score"])
        + len(shared_title_tokens) * int(config.get("title_keyword_score", 1))
    )


def update_related(config: dict[str, Any]) -> int:
    notes = load_notes()
    threshold = int(config["related_threshold"])
    relations: dict[Path, set[str]] = {
        path: set(metadata.get("related") or [])
        for path, metadata, _body in notes
    }

    for index, (left_path, left_meta, _left_body) in enumerate(notes):
        for right_path, right_meta, _right_body in notes[index + 1 :]:
            if relation_score(left_meta, right_meta, config) >= threshold:
                relations[left_path].add(right_path.name)
                relations[right_path].add(left_path.name)

    updated = 0
    for path, metadata, body in notes:
        new_related = sorted(relations[path])
        if new_related != sorted(metadata.get("related") or []):
            metadata["related"] = new_related
            metadata["updated"] = date.today().isoformat()
            write_note(path, metadata, body)
            updated += 1
    return updated


def review_priority(
    concept: str,
    entries: list[tuple[Path, dict[str, Any], str]],
    config: dict[str, Any],
) -> tuple[int, list[str]]:
    today = date.today()
    project_tags = {str(value).casefold() for value in config.get("project_tags", [])}
    score = len(entries) * 3
    reasons = [f"在 {len(entries)} 篇笔记中出现"]

    last_dates = [
        parsed
        for _path, metadata, _body in entries
        if (parsed := parse_iso_date((metadata.get("review") or {}).get("last_reviewed")))
    ]
    if not last_dates:
        score += 3
        reasons.append("尚无复习记录")
    else:
        days = (today - max(last_dates)).days
        if days >= 30:
            score += 3
            reasons.append(f"距上次复习 {days} 天")
        elif days >= 14:
            score += 2
            reasons.append(f"距上次复习 {days} 天")
        elif days >= 7:
            score += 1
            reasons.append(f"距上次复习 {days} 天")

    due_dates = [
        parsed
        for _path, metadata, _body in entries
        if (parsed := parse_iso_date((metadata.get("review") or {}).get("next_review")))
    ]
    if due_dates and min(due_dates) <= today:
        score += 4
        reasons.append("已到计划复习日期")

    if any(
        project_tags
        & {
            str(value).casefold()
            for value in [*(metadata.get("tags") or []), *(metadata.get("keywords") or [])]
        }
        for _path, metadata, _body in entries
    ):
        score += 2
        reasons.append("与当前项目标签相关")

    practice_markers = ("实践", "练习", "项目化", "动手", "已验证", "应用案例")
    if not any(
        any(marker in body for marker in practice_markers)
        for _path, _metadata, body in entries
    ):
        score += 2
        reasons.append("相关笔记缺少实践记录")

    return score, reasons


def build_review_list() -> Path:
    concept_counts: Counter[str] = Counter()
    candidates: dict[str, list[tuple[Path, dict[str, Any], str]]] = {}
    config = load_config()

    for path, metadata, body in load_notes():
        review = metadata.get("review") or {}
        if review.get("status") in {"mastered", "archived"}:
            continue
        for concept in review.get("concepts") or []:
            concept_counts[concept] += 1
            candidates.setdefault(concept, []).append((path, metadata, body))

    day = date.today().isoformat()
    output = ROOT / "reviews" / f"{day}-review-list.md"
    lines = [
        f"# {day} 待复习知识点",
        "",
        "> 此列表按出现频率、复习时间、项目相关性和实践记录进行规则排序。",
        "",
    ]

    if not concept_counts:
        lines.append("当前没有已标注的复习知识点。请先让 AI 完善笔记的 `review.concepts`。")
    else:
        ranked = sorted(
            (
                (review_priority(concept, entries, config), concept, entries)
                for concept, entries in candidates.items()
            ),
            key=lambda item: (-item[0][0], item[1].casefold()),
        )
        for (score, reasons), concept, entries in ranked:
            sources = ", ".join(path.name for path, _metadata, _body in entries)
            lines.extend(
                [
                    f"## {concept}",
                    "",
                    f"- 优先级分数：{score}",
                    f"- 出现次数：{concept_counts[concept]}",
                    f"- 来源笔记：{sources}",
                    f"- 推荐原因：{'；'.join(reasons)}。",
                    "",
                ]
            )

    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output


def build_topic_index() -> Path:
    topics: dict[str, list[tuple[Path, dict[str, Any], str]]] = {}
    for path, metadata, body in load_notes():
        for topic in metadata.get("tags") or []:
            cleaned = str(topic).strip()
            if cleaned:
                topics.setdefault(cleaned, []).append((path, metadata, body))

    output = ROOT / "wiki" / "_自动主题索引.md"
    lines = [
        "# 自动主题索引",
        "",
        f"> 最近更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "此页由 `scripts/fuxi.py topics` 根据笔记标签生成，不覆盖 AI 编写的主题页。",
        "",
    ]
    if not topics:
        lines.append("当前没有可聚合的标签。")
    else:
        for topic, entries in sorted(
            topics.items(),
            key=lambda item: (-len(item[1]), item[0].casefold()),
        ):
            lines.extend([f"## {topic}", ""])
            for path, metadata, body in entries:
                summary = note_summary(body) or "暂无摘要"
                lines.append(
                    f"- [{metadata.get('title', path.stem)}](../notes/{path.name})：{summary}"
                )
            lines.append("")

    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output


def search_documents(query: str, limit: int = 20) -> list[tuple[int, str, Path, str]]:
    terms = [term.casefold() for term in TOKEN_PATTERN.findall(query)]
    if not terms:
        terms = [query.strip().casefold()]

    results: list[tuple[int, str, Path, str]] = []
    search_roots = (
        ("wiki", ROOT / "wiki"),
        ("notes", ROOT / "notes"),
        ("reviews", ROOT / "reviews"),
        ("briefs", ROOT / "briefs"),
    )
    for kind, directory in search_roots:
        for path in sorted(directory.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            metadata, body = parse_frontmatter(text)
            title = str(metadata.get("title") or path.stem)
            title_folded = title.casefold()
            review = metadata.get("review") or {}
            tags = " ".join(
                [
                    *(metadata.get("tags") or []),
                    *(metadata.get("keywords") or []),
                    *(review.get("concepts") or []),
                ]
            ).casefold()
            body_folded = body.casefold()
            score = 0
            for term in terms:
                if term in title_folded:
                    score += 6
                if term in tags:
                    score += 4
                score += min(body_folded.count(term), 3)
            if score:
                snippet = note_summary(body) or compact_text(
                    " ".join(first_meaningful_lines(body, limit=2)),
                    100,
                )
                results.append((score, kind, path, snippet))

    index_path = ROOT / "INDEX.md"
    if index_path.exists():
        text = index_path.read_text(encoding="utf-8", errors="replace")
        folded = text.casefold()
        score = sum(min(folded.count(term), 3) for term in terms)
        if score:
            results.append(
                (
                    score,
                    "index",
                    index_path,
                    compact_text(" ".join(first_meaningful_lines(text, limit=2)), 100),
                )
            )

    results.sort(key=lambda item: (-item[0], item[1], item[2].name.casefold()))
    return results[:limit]


def command_search(query: str, limit: int) -> None:
    results = search_documents(query, limit)
    if not results:
        print(f"没有找到与“{query}”匹配的资料。")
        return
    for score, kind, path, snippet in results:
        relative = path.relative_to(ROOT).as_posix()
        print(f"[{score:02d}] {kind}: {relative}")
        if snippet:
            print(f"     {snippet}")


def validate_notes() -> list[str]:
    errors: list[str] = []
    required = {"title", "type", "source", "created", "updated", "tags", "keywords", "related"}
    for path in sorted((ROOT / "notes").glob("*.md")):
        metadata, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
        missing = sorted(required - set(metadata))
        if missing:
            errors.append(f"{path.relative_to(ROOT)} 缺少字段：{', '.join(missing)}")
        review = metadata.get("review")
        if not isinstance(review, dict):
            errors.append(f"{path.relative_to(ROOT)} 缺少 review 对象")
            continue
        if "concepts" not in review:
            errors.append(f"{path.relative_to(ROOT)} 缺少 review.concepts")
    return errors


def command_init() -> None:
    for directory in ("raw", "notes", "wiki", "briefs", "reviews", "scripts"):
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    topics = build_topic_index()
    index = build_index()
    print(f"已初始化：{ROOT}")
    print(f"索引：{index}")
    print(f"主题索引：{topics}")


def command_ingest(source_value: str) -> None:
    source = Path(source_value).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"输入路径不存在：{source}")

    config = load_config()
    files = list(iter_source_files(source, config))
    if not files:
        print("没有发现可处理的文本或 Markdown 文件。")
        return

    for path in files:
        raw_path, note_path = ingest_file(path)
        print(f"入库：{path}")
        print(f"  raw: {raw_path.relative_to(ROOT)}")
        print(f"  note: {note_path.relative_to(ROOT)}")

    updated = update_related(config)
    topics = build_topic_index()
    index = build_index()
    print(f"完成：{len(files)} 个文件，更新 {updated} 篇关联笔记。")
    print(f"索引：{index}")
    print(f"主题索引：{topics}")
    print("下一步：让 AI 按 AGENTS.md 完善新笔记的语义内容。")


def command_idea(text: str, note_type: str) -> None:
    day = date.today().isoformat()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    title = text.strip().splitlines()[0][:40] or "未命名想法"
    path = ROOT / "notes" / f"{day}-{safe_slug(title)}-{digest}.md"
    if path.exists():
        print(f"已存在：{path}")
        return

    metadata = {
        "title": title,
        "type": note_type,
        "source": "direct_input",
        "created": day,
        "updated": day,
        "tags": [],
        "keywords": [],
        "related": [],
        "review": {
            "status": "candidate",
            "concepts": [],
            "last_reviewed": "",
            "next_review": "",
        },
    }
    body = f"""# 原始输入

{text.strip()}

# 整理结果

等待 AI 按内容类型整理。

# 项目关联

等待 AI 判断。

# 需要复习的知识点

等待 AI 识别。
"""
    write_note(path, metadata, body)
    update_related(load_config())
    build_topic_index()
    build_index()
    print(f"已创建：{path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="fuxi 本地知识库机械工作流")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="初始化目录和索引")

    ingest = subparsers.add_parser("ingest", help="入库一个文件或文件夹")
    ingest.add_argument("source", help="文件或文件夹路径")

    idea = subparsers.add_parser("idea", help="记录一句话、灵感或任务")
    idea.add_argument("text", help="要记录的内容")
    idea.add_argument(
        "--type",
        choices=("idea_note", "task_note", "learning_note"),
        default="idea_note",
        help="笔记类型",
    )

    subparsers.add_parser("index", help="重建 INDEX.md")
    subparsers.add_parser("related", help="重新计算笔记关联")
    subparsers.add_parser("topics", help="按标签生成自动主题索引")
    subparsers.add_parser("review-list", help="生成待复习知识点列表")
    search = subparsers.add_parser("search", help="检索主题页、笔记、复习和选题")
    search.add_argument("query", help="检索关键词")
    search.add_argument("--limit", type=int, default=20, help="最多返回多少条结果")
    subparsers.add_parser("validate", help="检查 notes frontmatter")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "init":
            command_init()
        elif args.command == "ingest":
            command_ingest(args.source)
        elif args.command == "idea":
            command_idea(args.text, args.type)
        elif args.command == "index":
            print(f"索引：{build_index()}")
        elif args.command == "related":
            print(f"更新关联笔记：{update_related(load_config())}")
            build_topic_index()
            build_index()
        elif args.command == "topics":
            print(f"主题索引：{build_topic_index()}")
        elif args.command == "review-list":
            print(f"复习列表：{build_review_list()}")
        elif args.command == "search":
            command_search(args.query, args.limit)
        elif args.command == "validate":
            errors = validate_notes()
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("检查通过。")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
