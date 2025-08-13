{% if cookiecutter.css_framework == 'tailwindcss' -%}
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
{%- endif %}