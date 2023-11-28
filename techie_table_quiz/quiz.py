from pathlib import Path
import shutil

from pydantic import BaseModel, Field
from pydantic_yaml import parse_yaml_raw_as
import structlog

LOG = structlog.get_logger()


class Question(BaseModel):
    question: str
    question_image: str | None = None
    answer: str
    answer_image: str | None = None
    number: int = 0
    sources: list[str] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)


class Round(BaseModel):
    title: str
    questions: list[Question]
    number: int = 0

    def update(self):
        for i, question in enumerate(self.questions):
            question.number = i + 1

    def copy_images(self, source: Path, destination: Path, answer_mode: bool):
        for question in self.questions:
            images = (
                [question.question_image, question.answer_image]
                if answer_mode
                else [question.question_image]
            )
            images.extend(question.images)
            for filename in images:
                if filename is None:
                    continue
                destination.mkdir(exist_ok=True, parents=True)
                source_path = source / filename
                destination_path = destination / filename
                LOG.info(
                    "copy_images",
                    question=question.number,
                    source=source_path,
                    destination=destination_path,
                )
                shutil.copyfile(source_path, destination_path)


class Quiz(BaseModel):
    rounds: list[Round]

    def update(self):
        for i, round in enumerate(self.rounds):
            round.update()
            round.number = i + 1

    def copy_images(self, source: Path, destination: Path, answer_mode: bool):
        for round in self.rounds:
            round.copy_images(
                source=source, destination=destination, answer_mode=answer_mode
            )


def parse_yaml(yaml: str) -> Quiz:
    quiz = parse_yaml_raw_as(Quiz, yaml)
    quiz.update()
    return quiz
