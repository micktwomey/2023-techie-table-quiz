{%- from 'macros/question.md' import ask_question, answer_question -%}
{%- from 'macros/theme.md' import theme -%}
{{ theme(3) }}

{% for round in quiz.rounds %}

# {{round.title}}
## Answers

---

{% for question in round.questions %}
{{ ask_question(question=question) }}
---
{{ answer_question(question=question) }}
---
{% endfor %}

{% endfor %}
