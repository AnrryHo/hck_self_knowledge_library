#!/usr/bin/env python3
"""End-to-end smoke test for the local fuxi CLI."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_cli(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(root / "scripts" / "fuxi.py"), *arguments],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def load_fuxi(root: Path):
    spec = importlib.util.spec_from_file_location(
        "fuxi_smoke_module",
        root / "scripts" / "fuxi.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载 fuxi.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def enrich_note(module, path: Path, tags: list[str], keywords: list[str], concept: str) -> None:
    metadata, body = module.parse_frontmatter(path.read_text(encoding="utf-8"))
    metadata["tags"] = tags
    metadata["keywords"] = keywords
    metadata["review"]["concepts"] = [concept]
    module.write_note(path, metadata, body)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="fuxi-smoke-") as temp_value:
        root = Path(temp_value)
        shutil.copytree(
            PROJECT_ROOT,
            root,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        for directory_name in ("raw", "notes", "wiki", "briefs", "reviews"):
            directory = root / directory_name
            shutil.rmtree(directory)
            directory.mkdir()

        source_dir = root / "smoke-input"
        source_dir.mkdir()
        (source_dir / "agent-memory.md").write_text(
            "# Agent Memory\n\nAgent memory includes short-term and long-term memory.\n",
            encoding="utf-8",
        )
        (source_dir / "agent-planning.txt").write_text(
            "Agent planning uses goals, tools, and execution feedback.\n",
            encoding="utf-8",
        )

        run_cli(root, "init")
        run_cli(root, "ingest", str(source_dir / "agent-memory.md"))
        run_cli(root, "ingest", str(source_dir))
        run_cli(root, "idea", "完成 Agent 项目的记忆模块", "--type", "task_note")

        notes = sorted((root / "notes").glob("*.md"))
        raw_files = sorted(path for path in (root / "raw").glob("*.*") if path.name != ".gitkeep")
        assert len(notes) == 3, f"预期 3 篇笔记，实际 {len(notes)}"
        assert len(raw_files) == 2, f"预期 2 份 raw，实际 {len(raw_files)}"

        module = load_fuxi(root)
        source_notes = [
            path
            for path in notes
            if module.parse_frontmatter(path.read_text(encoding="utf-8"))[0].get("type")
            == "source_note"
        ]
        assert len(source_notes) == 2

        enrich_note(
            module,
            source_notes[0],
            ["AI Agent", "学习"],
            ["memory", "agent"],
            "Agent 记忆",
        )
        enrich_note(
            module,
            source_notes[1],
            ["AI Agent", "学习"],
            ["planning", "agent"],
            "Agent 规划",
        )

        related_result = run_cli(root, "related")
        assert "更新关联笔记：2" in related_result.stdout
        run_cli(root, "index")
        run_cli(root, "topics")
        run_cli(root, "review-list")
        run_cli(root, "validate")

        for path in source_notes:
            metadata, _body = module.parse_frontmatter(path.read_text(encoding="utf-8"))
            assert len(metadata["related"]) == 1

        index_text = (root / "INDEX.md").read_text(encoding="utf-8")
        assert "Agent 记忆" in index_text
        assert "Agent 规划" in index_text
        assert "摘要" in index_text
        assert "复习状态" in index_text
        assert "Agent memory includes short-term" in index_text

        topic_text = (root / "wiki" / "_自动主题索引.md").read_text(encoding="utf-8")
        assert "## AI Agent" in topic_text
        assert "agent-memory" in topic_text
        assert "agent-planning" in topic_text

        search_result = run_cli(root, "search", "Agent 记忆")
        assert "notes/" in search_result.stdout
        assert "agent-memory" in search_result.stdout

        review_files = list((root / "reviews").glob("*-review-list.md"))
        assert len(review_files) == 1
        review_text = review_files[0].read_text(encoding="utf-8")
        assert "Agent 记忆" in review_text
        assert "Agent 规划" in review_text
        assert "优先级分数" in review_text
        assert "尚无复习记录" in review_text
        assert "缺少实践记录" in review_text

        config = json.loads((root / "fuxi.config.json").read_text(encoding="utf-8"))
        assert config["related_threshold"] == 4
        title_score = module.relation_score(
            {"title": "Agent Memory", "tags": [], "keywords": []},
            {"title": "Agent Planning", "tags": [], "keywords": []},
            config,
        )
        assert title_score == config["title_keyword_score"]

    print("fuxi 冒烟测试通过。")
    print(
        "覆盖：初始化、文件/文件夹入库、去重、想法、索引、关联、"
        "主题聚合、检索、复习排序、校验。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
