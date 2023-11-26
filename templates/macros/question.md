{% macro ask_question(question) -%}
# Question {{question.number}}
{{question.question}}
{% if question.question_image %}
{% if question.number is even %}
![left]({{question.question_image}})
{% else %}
![right]({{question.question_image}})
{% endif %}
{% endif %}
{%- endmacro %}

{% macro answer_question(question) -%}
# Question {{question.number}} Answer
{{question.question}}
{{question.answer}}
{% if question.answer_image %}
{% if question.number is even %}
![left]({{question.answer_image}})
{% else %}
![right]({{question.answer_image}})
{% endif %}
{% endif %}
{%- endmacro %}
