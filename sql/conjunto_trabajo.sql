/*
Conjunto de trabajo RFM.

Los identificadores se escriben como tokens canónicos y se resuelven desde
esquema.py. Recencia se mide contra la fecha máxima registrada en la base,
nunca contra GETDATE(), para que el resultado sea reproducible.
*/
WITH FechaMax AS (
    SELECT MAX({{rental.rental_date}}) AS max_fecha
    FROM {{rental}}
)
SELECT
    c.{{customer.customer_id}} AS customer_id,
    CONCAT(c.{{customer.first_name}}, ' ', c.{{customer.last_name}}) AS customer_name,
    DATEDIFF(day, MAX(a.{{rental.rental_date}}), fm.max_fecha) AS recency_days,
    COUNT(DISTINCT a.{{rental.rental_id}}) AS rental_frequency,
    COALESCE(SUM(p.{{payment.amount}}), 0) AS monetary_amount
FROM {{customer}} AS c
LEFT JOIN {{rental}} AS a
    ON a.{{rental.customer_id}} = c.{{customer.customer_id}}
LEFT JOIN {{payment}} AS p
    ON p.{{payment.rental_id}} = a.{{rental.rental_id}}
CROSS JOIN FechaMax AS fm
GROUP BY
    c.{{customer.customer_id}},
    c.{{customer.first_name}},
    c.{{customer.last_name}},
    fm.max_fecha;
