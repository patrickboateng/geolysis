{% if obj.short_name == "round_" %}

.. autodecorator:: {{ obj.short_name }}

{% else %}

.. autofunction:: {{ obj.short_name }}

{% endif %}
