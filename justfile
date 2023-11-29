

build:
  poetry run techie-table-quiz build

watch:
  poetry run techie-table-quiz watch

statistics:
  poetry run techie-table-quiz statistics

export-to-pdf: build
  mkdir -p pdf
  poetry run techie-table-quiz generate-pdf output/answers/quiz/quiz.md pdf/quiz_answers.pdf
  poetry run techie-table-quiz generate-pdf output/answers/round_1/round_1_answers.md pdf/round_1_answers.pdf
  poetry run techie-table-quiz generate-pdf output/answers/round_2/round_2_answers.md pdf/round_2_answers.pdf
  poetry run techie-table-quiz generate-pdf output/answers/round_3/round_3_answers.md pdf/round_3_answers.pdf
  poetry run techie-table-quiz generate-pdf output/answers/round_4/round_4_answers.md pdf/round_4_answers.pdf
  poetry run techie-table-quiz generate-pdf output/answers/tie-breaker/tie-breaker_answers.md pdf/tie-breaker_answers.pdf
  poetry run techie-table-quiz generate-pdf output/questions/quiz/quiz.md pdf/quiz_questions.pdf
  poetry run techie-table-quiz generate-pdf output/questions/round_1/round_1_questions.md  pdf/round_1_questions.pdf
  poetry run techie-table-quiz generate-pdf output/questions/round_2/round_2_questions.md  pdf/round_2_questions.pdf
  poetry run techie-table-quiz generate-pdf output/questions/round_3/round_3_questions.md  pdf/round_3_questions.pdf
  poetry run techie-table-quiz generate-pdf output/questions/round_4/round_4_questions.md  pdf/round_4_questions.pdf
  poetry run techie-table-quiz generate-pdf output/questions/tie-breaker/tie-breaker_questions.md  pdf/tie-breaker_questions.pdf
