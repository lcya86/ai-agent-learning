import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


class WorkItem(BaseModel):
    title: str
    evidence: list[str] = Field(default_factory=list)


class ReportDraft(BaseModel):
    highlights: list[WorkItem] = Field(default_factory=list)
    progress: list[WorkItem] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    plan: list[str] = Field(default_factory=list)


@dataclass(frozen=True)
class ModelConfig:
    model: str
    base_url: str | None


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "command failed")
    return p.stdout


def git_log_since(repo: Path, since: datetime) -> str:
    return run(
        [
            "git",
            "-C",
            str(repo),
            "log",
            "--since",
            since.isoformat(),
            "--pretty=format:%h|%ad|%s",
            "--date=short",
        ]
    )


def read_notes(notes_dir: Path) -> str:
    if not notes_dir.exists():
        return ""
    parts: list[str] = []
    for p in sorted(notes_dir.glob("*.md")):
        parts.append(f"## {p.name}\n" + p.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def build_client() -> tuple[OpenAI, ModelConfig]:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
    model = os.getenv("OPENAI_MODEL", "deepseek-ai/DeepSeek-V3.2")
    return OpenAI(api_key=api_key, base_url=base_url), ModelConfig(model=model, base_url=base_url)


def llm_draft(client: OpenAI, cfg: ModelConfig, raw_git: str, raw_notes: str, kind: str, for_date: str) -> ReportDraft:
    schema = ReportDraft.model_json_schema()
    sys = "你是一个工程师日报/周报生成Agent。只输出JSON，不要输出多余文本。"
    user = {
        "kind": kind,
        "date": for_date,
        "inputs": {
            "git_log": raw_git,
            "notes": raw_notes,
        },
        "instructions": [
            "基于证据写内容，避免编造；没有证据就不要写。",
            "把git提交按主题合并成工作项，标题要像可汇报的事项。",
            "evidence里保留原始提交行或notes引用。",
            "blockers/plan允许来自notes，也可为空。",
        ],
        "output_schema": schema,
    }

    r = client.chat.completions.create(
        model=cfg.model,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    )
    return ReportDraft.model_validate_json(r.choices[0].message.content)


def llm_check_and_repair(client: OpenAI, cfg: ModelConfig, draft: ReportDraft, raw_git: str, raw_notes: str) -> ReportDraft:
    schema = ReportDraft.model_json_schema()
    sys = "你是严格的审校Agent。只输出JSON，不要输出多余文本。"
    user = {
        "draft": draft.model_dump(),
        "inputs": {"git_log": raw_git, "notes": raw_notes},
        "checks": [
            "删除没有证据支撑的条目（evidence为空的work item优先删除或补证据）。",
            "合并重复/相似条目，标题更清晰。",
            "确保字段符合schema，列表不要为null。",
        ],
        "output_schema": schema,
    }
    r = client.chat.completions.create(
        model=cfg.model,
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    )
    return ReportDraft.model_validate_json(r.choices[0].message.content)


def render_md(draft: ReportDraft, title: str) -> str:
    def render_items(items: list[WorkItem]) -> str:
        if not items:
            return "- （无）"
        lines: list[str] = []
        for it in items:
            lines.append(f"- {it.title}")
            for ev in it.evidence[:5]:
                lines.append(f"  - 证据：{ev}")
        return "\n".join(lines)

    blockers = "\n".join([f"- {b}" for b in draft.blockers]) or "- （无）"
    plan = "\n".join([f"- {p}" for p in draft.plan]) or "- （无）"

    return "\n".join(
        [
            f"# {title}",
            "",
            "## 亮点",
            render_items(draft.highlights),
            "",
            "## 进展",
            render_items(draft.progress),
            "",
            "## 阻塞",
            blockers,
            "",
            "## 明日/下周计划",
            plan,
            "",
        ]
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--notes", default="notes")
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--kind", choices=["daily", "weekly"], default="daily")
    ap.add_argument("--days", type=int, default=None)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    notes_dir = Path(args.notes).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.days is None:
        days = 1 if args.kind == "daily" else 7
    else:
        days = args.days

    since = datetime.now() - timedelta(days=days)
    raw_git = git_log_since(repo, since)
    raw_notes = read_notes(notes_dir)

    client, cfg = build_client()

    for_date = date.today().isoformat()
    draft = llm_draft(client, cfg, raw_git, raw_notes, args.kind, for_date)
    draft2 = llm_check_and_repair(client, cfg, draft, raw_git, raw_notes)

    title = f"日报 {for_date}" if args.kind == "daily" else f"周报 {for_date}"
    md = render_md(draft2, title)

    out_name = f"daily_{for_date}.md" if args.kind == "daily" else f"weekly_{for_date}.md"
    (out_dir / out_name).write_text(md, encoding="utf-8")

    trace = {
        "kind": args.kind,
        "date": for_date,
        "since": since.isoformat(),
        "model": cfg.model,
        "raw_git": raw_git,
        "raw_notes": raw_notes,
        "draft": draft.model_dump(),
        "final": draft2.model_dump(),
    }
    (out_dir / (out_name + ".trace.json")).write_text(json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8")

    print(str(out_dir / out_name))


if __name__ == "__main__":
    main()
