import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentResult:
    name: str
    status: str
    warnings: list[str]


class BaseAgent:
    name = "base-agent"

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.name)

    def result(self, status: str = "ok", warnings: list[str] | None = None) -> AgentResult:
        return AgentResult(name=self.name, status=status, warnings=warnings or [])

