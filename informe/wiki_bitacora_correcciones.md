# 30/10/2026 - Correcciones a partir de la devolución

Se preparó una revisión del TP2 con apoyo de IA y se verificaron los
resultados para la defensa del 19/11. La distribución y aprobación de estos
cambios debe confirmarse con los integrantes, sin inferir autoría individual.

- Se contaron las filas del archivo de carga de TP1: 16.044 pagos, máximo
  identificador 16.049 y cinco huecos de ID. La reconciliación da diferencia
  cero. Se retiró la explicación de pagos perdidos.
- Se agregaron reglas de devolución anterior al alquiler y pago anterior al
  alquiler, calculadas tanto en SQL Server como en pandas.
- Se alineó el monto del pipeline con la consulta del notebook y se adoptó
  el nombre `pipeline_tp2.py`.
- Se guardó evidencia de dos ejecuciones del archivo final: conteos, sumas,
  comparación completa de negocio y huella del código ejecutado.
- Se reemplazó el hallazgo monto-frecuencia por monto por alquiler y se
  concretó un piloto comercial para evaluar, sin afirmar causalidad.
- Se actualizaron informe y diagnóstico. Se preparó una guía para que cada
  integrante explique y ejecute el proyecto completo.

Repositorio: https://github.com/NICKMC500/TP2-Equipo1_RFM

La versión corregida y sus evidencias se identificarán por el commit que
el equipo acuerde publicar. Esta nota no presenta cambios locales como si
ya estuvieran publicados en GitHub.
