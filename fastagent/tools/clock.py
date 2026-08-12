"""时间查询 Skill：返回当前时间。"""

from __future__ import annotations

from datetime import datetime, timezone

from ..skill import Skill


class ClockSkill(Skill):
    """返回当前 UTC 时间的 ISO 8601 字符串，可选自定义 strftime 格式。"""

    name = "clock"
    description = "获取当前时间，可选传入 fmt（strftime 格式）"

    async def run(self, fmt: str | None = None) -> str:
        now = datetime.now(timezone.utc)
        if fmt:
            return now.strftime(fmt)
        return now.isoformat()
