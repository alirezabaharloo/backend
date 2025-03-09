{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hi {{ email }}
{% endblock %}

{% block body %}
<p>for resset your password <a href="http://localhost:8000/resset_password/check/{{ token }}">click here</a></p>
{% endblock %}

