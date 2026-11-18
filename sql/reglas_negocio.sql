/* Reglas temporales del dominio, independientes de la fórmula de recencia. */
SELECT
    (SELECT COUNT_BIG(*) FROM {{rental}} AS r
     WHERE r.{{rental.return_date}} < r.{{rental.rental_date}}) AS return_before_rental,
    (SELECT COUNT_BIG(*) FROM {{payment}} AS p
     INNER JOIN {{rental}} AS r ON p.{{payment.rental_id}} = r.{{rental.rental_id}}
     WHERE p.{{payment.payment_date}} < r.{{rental.rental_date}}) AS payment_before_rental,
    (SELECT COUNT_BIG(*) FROM {{payment}} AS p
     WHERE p.{{payment.amount}} < 0) AS negative_payments;
