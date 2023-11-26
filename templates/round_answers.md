{%- from 'macros/question.md' import ask_question, answer_question -%}
{%- from 'macros/theme.md' import theme -%}
{{ theme(round) }}


# {{round.title}}
## Answers

---

{% for question in round.questions %}
{{ ask_question(question=question) }}
---
{{ answer_question(question=question) }}
---
{% endfor %}
