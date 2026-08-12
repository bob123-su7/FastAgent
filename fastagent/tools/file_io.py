"""文件读写 Skill：在指定根目录内安全地读写文本文件。"""

from __future__ import annotations

from pathlib import Path

from ..skill import Skill


def _resolve_within_root(root: Path, relative_path: str) -> Path:
    """将 relative_path 解析为 root 下的绝对路径，禁止越权访问 root 之外的路径。"""
    target = (root / relative_path).resolve()
    root_resolved = root.resolve()
    if root_resolved not in target.parents and target != root_resolved:
        raise ValueError(f"路径 '{relative_path}' 超出允许的根目录范围")
    return target


class ReadFileSkill(Skill):
    """读取根目录下某个文本文件的内容。"""

    name = "read_file"
    description = "读取指定根目录下某个文本文件的内容，参数为相对路径 path"

    def __init__(self, root: str | Path = ".") -> None:
        self._root = Path(root)

    async def run(self, path: str) -> str:
        target = _resolve_within_root(self._root, path)
        return target.read_text(encoding="utf-8")


class WriteFileSkill(Skill):
    """向根目录下某个文本文件写入内容（覆盖写入）。"""

    name = "write_file"
    description = "向指定根目录下某个文本文件写入内容，参数为相对路径 path 与文本 content"

    def __init__(self, root: str | Path = ".") -> None:
        self._root = Path(root)

    async def run(self, path: str, content: str) -> str:
        target = _resolve_within_root(self._root, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"已写入 {target}"
