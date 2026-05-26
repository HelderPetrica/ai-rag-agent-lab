from app.agents.answer_agent import AnswerAgent
from app.agents.validation_agent import ValidationAgent


def test_answer_agent_reports_missing_context() -> None:
    answer = AnswerAgent().answer("What happened?", [])

    assert "do not have enough indexed context" in answer


def test_validation_agent_flags_missing_context() -> None:
    confidence, warnings = ValidationAgent().validate("No context answer", [])

    assert confidence == 0.0
    assert warnings


def test_validation_agent_flags_low_confidence_context() -> None:
    class Chunk:
        source = "unit-test"

    class Result:
        chunk = Chunk()
        score = 0.1

    confidence, warnings = ValidationAgent().validate("Grounded answer", [Result()])

    assert confidence > 0
    assert any("Low retrieval score" in warning for warning in warnings)
