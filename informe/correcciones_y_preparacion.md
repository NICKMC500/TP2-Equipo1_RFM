# Correcciones posteriores a la devolución del TP2

Fecha de preparación: 30/10/2026. La entrega original evaluada fue 957e3c9.
Los cambios se preparan en la copia de main del usuario; no se alteran las
ramas de los compañeros ni se atribuyen a ellos nuevos commits.

| Observación | Corrección y evidencia |
| --- | --- |
| Conteos de origen escritos a mano | Conteo del archivo exacto de TP1 mediante `reconciliar_origen.py`; procedencia y SHA-256 en `evidencia_reconciliacion.json`. |
| Cinco pagos supuestamente perdidos | 16.044 tuplas y máximo ID 16.049. Los huecos no representan pérdida en la migración. |
| Reglas débiles | Devolución anterior al alquiler y pago anterior al alquiler, contrastadas en SQL y pandas. |
| Hallazgo casi tautológico | Promedio por cliente de monto / alquileres por quintil; gráfico narrativo con base cero. |
| Decisión comercial vaga | Piloto para el tramo central de gasto, con grupo de control y nuevos alquileres a 30 días como evaluación propuesta. |
| Monto distinto en ETL y notebook | Ambas consultas suman pagos a través del alquiler. |
| Evidencia de script viejo | Dos ejecuciones CLI del archivo final y huella de su código. |
| Idempotencia con solo conteo | Consulta independiente con conteos y sumas, igualdad completa de negocio y SHA-256; auditoría temporal excluida. |
| Nombre de archivo | `pipeline/pipeline_tp2.py`. |
| Wiki incompleta | Textos de diccionario con tablas, columnas y reconciliación, y nota de correcciones, preparados para publicar. |

## Cómo practicar el oral

1. Cada integrante ejecuta el notebook completo en `venv_tp2` y explica una
   comparación SQL-pandas, una regla y cada gráfico.
2. Cada integrante ejecuta `python pipeline/pipeline_tp2.py` desde la raíz
   y después `python pipeline/verificar_idempotencia.py`. Explica qué tabla
   se reemplaza y por qué `append` no acumula clientes después del DELETE.
3. Ensayar el cambio de mapeo para otra base equivalente: cambiar los nombres
   físicos en `esquema.py`, configurar la conexión por variables de entorno
   y volver a renderizar las consultas. No cambiar una base real durante el
   ensayo sin acordar cuál se utiliza.
4. Responder: por qué quintiles relativos, qué ocurre con empates y por qué
   recencia se mide contra la fecha máxima del dataset.
5. Explicar los límites: dataset de ejemplo, CSV ficticio, ticket medio no
   es rentabilidad y un piloto propuesto no demuestra efecto comercial.

La corrección usa los scripts traducidos de TP1 aportados por el equipo.
La reconstrucción de `film_text` por trigger se declara y se acredita con el
DDL; no se cuenta como un INSERT directo del archivo de carga.

## Pendiente fuera del repositorio

Revisar y publicar los textos de la wiki en el aula, confirmar las
contribuciones reales de cada integrante y acordar la versión corregida que
se presentará en la defensa. Las mejoras de código no sustituyen ese ensayo.
