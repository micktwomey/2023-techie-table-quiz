{%- from 'macros/question.md' import ask_question -%}
{%- from 'macros/theme.md' import theme -%}
{{ theme(2) }}

{% for round in quiz.rounds %}

# {{round.title}}
## Questions

---

{% for question in round.questions %}
{{ ask_question(question=question) }}
---
{% endfor %}

{% endfor %}
