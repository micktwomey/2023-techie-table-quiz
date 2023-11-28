from pathlib import Path
import subprocess
import tempfile

import jinja2
import rich.traceback
import structlog
import typer
import watchfiles

from .quiz import parse_yaml, Quiz, Round

app = typer.Typer()
LOG = structlog.get_logger()


def convert_to_pdf(
    env: jinja2.Environment,
    markdown_path: Path,
    pdf_path: Path,
    print_all_steps: bool = False,
    include_presenter_notes: bool = False,
    template_filename="deckset_osascript.applescript",
):
    template = env.get_template(template_filename)
    with tempfile.NamedTemporaryFile(
        suffix=".applescript", delete_on_close=False
    ) as fp:
        output = template.render(
            markdown_abspath=str(markdown_path.absolute()),
            pdf_abspath=str(pdf_path.absolute()),
            print_all_steps="true" if print_all_steps else "false",
            include_presenter_notes="true" if include_presenter_notes else "false",
        )
        fp.write(output.encode("utf-8"))
        fp.close()

        subprocess.check_call(["osascript", fp.name])


@app.command()
def generate_pdf(
    input: Path,
    output: Path,
    print_all_steps: bool = False,
    include_presenter_notes: bool = False,
    templates_path: Path = Path("templates/"),
):
    """Convert markdown to PDF slides using Deckset"""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_path),
        autoescape=jinja2.select_autoescape(),
    )
    LOG.info(
        "convert_to_pdf",
        markdown_path=input,
        pdf_path=output,
        print_all_steps=print_all_steps,
        include_presenter_notes=include_presenter_notes,
    )
    convert_to_pdf(
        env=env,
        markdown_path=input,
        pdf_path=output,
        print_all_steps=print_all_steps,
        include_presenter_notes=include_presenter_notes,
    )


def generate_round(
    env: jinja2.Environment,
    round: Round,
    quiz: Quiz,
    template_filename: str,
    output_path: Path,
    images_path: Path,
    output_prefix: str,
    answer_mode: bool,
):
    template = env.get_template(template_filename)
    output = template.render(round=round, quiz=quiz)
    round_prefix = round.title.strip().lower().replace(" ", "_")
    p = (
        output_path
        / output_prefix
        / round_prefix
        / (round_prefix + "_" + output_prefix + ".md")
    )
    LOG.info(
        "generate_round",
        path=p,
        answer_mode=answer_mode,
        output_prefix=output_prefix,
        template=template,
    )
    p.parent.mkdir(exist_ok=True, parents=True)
    p.open("w").write(output)
    round.copy_images(
        source=images_path,
        destination=output_path / output_prefix / round_prefix,
        answer_mode=answer_mode,
    )


def generate_all_rounds(
    env: jinja2.Environment,
    quiz: Quiz,
    template_filename: str,
    output_path: Path,
    images_path: Path,
    output_prefix: str,
    answer_mode: bool,
):
    template = env.get_template(template_filename)
    output = template.render(round=round, quiz=quiz)
    p = output_path / output_prefix / "quiz" / "quiz.md"
    LOG.info(
        "generate_all_rounds",
        path=p,
        answer_mode=answer_mode,
        output_prefix=output_prefix,
        template=template,
    )
    p.parent.mkdir(exist_ok=True, parents=True)
    p.open("w").write(output)
    quiz.copy_images(
        source=images_path,
        destination=output_path / output_prefix / "quiz",
        answer_mode=answer_mode,
    )


def generate_quiz(
    templates_path: Path,
    questions_and_answers: Path,
    images_path: Path,
    output_path: Path,
):
    LOG.info(
        "generate_quiz",
        templates_path=templates_path,
        questions_and_answers=questions_and_answers,
        images_path=images_path,
        output_path=output_path,
    )
    quiz = parse_yaml(questions_and_answers.open("r").read())

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_path),
        autoescape=jinja2.select_autoescape(),
    )

    generate_all_rounds(
        env=env,
        quiz=quiz,
        template_filename="all_rounds_questions.md",
        output_path=output_path,
        images_path=images_path,
        output_prefix="questions",
        answer_mode=False,
    )

    generate_all_rounds(
        env=env,
        quiz=quiz,
        template_filename="all_rounds_answers.md",
        output_path=output_path,
        images_path=images_path,
        output_prefix="answers",
        answer_mode=True,
    )

    for round in quiz.rounds:
        generate_round(
            env=env,
            round=round,
            quiz=quiz,
            template_filename="round_questions.md",
            output_path=output_path,
            images_path=images_path,
            output_prefix="questions",
            answer_mode=False,
        )

        generate_round(
            env=env,
            round=round,
            quiz=quiz,
            template_filename="round_answers.md",
            output_path=output_path,
            images_path=images_path,
            output_prefix="answers",
            answer_mode=True,
        )


@app.command()
def build(
    templates_path: Path = Path("templates/"),
    questions_and_answers: Path = Path("questions_and_answers.yaml"),
    images_path: Path = Path("images"),
    output_path: Path = Path("output"),
):
    rich.traceback.install()
    generate_quiz(
        templates_path=templates_path,
        questions_and_answers=questions_and_answers,
        images_path=images_path,
        output_path=output_path,
    )


@app.command()
def watch(
    templates_path: Path = Path("templates/"),
    questions_and_answers: Path = Path("questions_and_answers.yaml"),
    images_path: Path = Path("images"),
    output_path: Path = Path("output"),
):
    rich.traceback.install()

    def watch_build():
        generate_quiz(
            templates_path=templates_path,
            questions_and_answers=questions_and_answers,
            images_path=images_path,
            output_path=output_path,
        )

    watch_build()
    for change in watchfiles.watch(
        templates_path,
        questions_and_answers,
        images_path,
    ):
        LOG.info("changed", change=change)
        watch_build()


@app.command()
def statistics(questions_and_answers: Path = Path("questions_and_answers.yaml")):
    """Generate some statistics"""
    quiz = parse_yaml(questions_and_answers.open("r").read())
    LOG.info("rounds", count=len(quiz.rounds))
    for round in quiz.rounds:
        try:
            LOG.info("questions", count=len(round.questions), round=round.number)
        except Exception:
            LOG.error("Skipping change")


if __name__ == "__main__":
    app()
