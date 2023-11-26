{% macro ask_question(question) -%}
# Question {{question.number}}
{{question.question}}
{% if question.question_image %}
{% if question.number is even %}
![left fit]({{question.question_image}})
{% else %}
![right fit]({{question.question_image}})
{% endif %}
{% endif %}
{%- endmacro %}

{% macro answer_question(question) -%}
# Question {{question.number}} Answer

{{question.answer}}

{% if question.answer_image %}
{% if question.number is even %}
![left fit]({{question.answer_image}})
{% else %}
![right fit]({{question.answer_image}})
{% endif %}
{% endif %}

{% for source in question.sources %}
- [`{{source}}`]({{source}})
{% endfor %}
{%- endmacro %}
