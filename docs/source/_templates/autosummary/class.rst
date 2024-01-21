{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :no-members:
   :no-inherited-members:
   :no-special-members:

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
      :toctree:

   {% for attr in attributes %}
      ~{{ name }}.{{ attr }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block methods %}

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
      :toctree: 
      :nosignatures:

   {% for method in methods %}
      {%- if not method.startswith('_') %}
         ~{{ name }}.{{ method }}
      {%- endif -%}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   