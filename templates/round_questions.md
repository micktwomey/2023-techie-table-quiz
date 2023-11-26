{%- from 'macros/question.md' import ask_question -%}
{%- from 'macros/theme.md' import theme -%}
{{ theme(round) }}

# {{round.title}}
## Questions

---

{% for question in round.questions %}
{{ ask_question(question=question) }}
---
{% endfor %}
