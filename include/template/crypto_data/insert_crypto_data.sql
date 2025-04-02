insert ignore into crypto_currency_value(
    id_crypto,
    crypto_name,
    crypto_symbol,
    date,
    price
)
values
{% set comma = joiner(',') %}
{% for record in base %}
    {{ comma() }}(
        '{{record.id}}',
        '{{record.name}}',
        '{{record.symbol}}',
        '{{record.date}}',
        {{record.price}}

     )
{% endfor %}
