ANEXO DE TRAZABILIDAD IA

1. Bitacora de prompts 

Errores y consuiltas  durante el desarrollo del notebook

Primer Prompt -  traceback enviado ProgrammingError: ('42000', "[42000] [Microsoft][ODBC Driver 18 for SQL Server][SQL Server]Incorrect syntax near 'go'. (102)..."), al intentar ejecutar conjunto_trabajo.sql desde Python.
 Para qué: entender por qué SQL Server rechazaba el archivo .sql al ejecutarlo con SQLAlchemy.

Segundo Prompt - traceback enviado ValueError: Bin edges must be unique: Index([0.0, 0.0, 175.0, 175.0, 176.0, 181.0]...)
Para qué: entender por qué pd.qcut fallaba. Los bordes repetidos mostraban que la recencia tiene muchos valores iguales (0 y 175), algo que después se documentó como limitación.

Tercer Prompt - traceback enviado KeyError: 'cliente_id', al hacer la verificación de duplicados y el resumen del DataFrame.
Para qué: corregir la diferencia entre el nombre de columna usado en el código (cliente_id) y el de la base en español (id_cliente).

Cuarto Prompt - traceback enviado . Solicitud de revisión para la Celda 4 (análisis IQR): código con q1_m = df_rfm["monto_total"].quantile(0.25) ... y print(f"Violaciones por Frecuencia <= 0: {len(regla_frecuencia_cero)}"), con la consigna "verifica la celda 4". 
Para qué: validar el análisis de valores atípicos por IQR y las reglas de negocio.

Quinto Prompt -  tracebak enviado NameError: name 'df_rfm' is not defined. 
Para qué: entender el error que apareció tras reiniciar el kernel, cuando la variable ya no estaba cargada.

Sexto Prompt - traceback enviado Confirmación de la salida de la Celda 4: Q1: $94.78 | Q3: $128.70 | IQR: $33.92 ... Violaciones por Monto Negativo: 0 | Violaciones por Frecuencia <= 0: 0. 
Para qué: confirmar que la salida era coherente con lo esperado.

Septimp Prompt - traceback enviado "La actividad 1 me tira esto."
Se informaron los errores NameError y luego una diferencia entre la recencia calculada en SQL Server y en pandas.
Para qué: diagnosticar por qué la validación entre SQL y pandas fallaba.

Octavo Prompt - traceback enviado "No deberían aparecer tablas con variables en inglés sino en español para guiarse, evitar estos errores es esencial." "Hay todavía variables en tablas como count, mean, min, como también el RangeIndex, los Non-Null Count, el dtype, el memory usage."
Para qué: que las salidas del notebook fueran claras y estuvieran en español.

Noveno Prompt - traceback enviado "Hagamos una última revisión y si no hay más inconvenientes podemos realizar el commit y el push al main."
Para qué: validar el proyecto antes de publicarlo.

Decimo prompt - Actualmente tenemos la base de datos cargada en SQL Server y venimos desarrollando las actividades anteriores. Queremos estructurar un script en Python (`pipeline.py`) que:
Extraiga la información de transacciones y clientes desde SQL Server.
Lea un archivo CSV complementario con datos del perfil comercial de los clientes (`perfil_comercial_clientes.csv`).
Combine y transforme los datos para calcular las métricas RFM (Recency, Frequency, Monetary).
Cargue el resultado en una tabla destino dentro de SQL Server, garantizando idempotencia.
Revisá el estado del repositorio y nuestro `README.md` para orientarte sobre lo que ya tenemos implementado.
Para que: un diseño conceptual de `pipeline.py` en cuatro etapas (extracción, transformación, carga con DELETE + INSERT dentro de una transacción para lograr idempotencia, y una función de orquestación con manejo de excepciones y logging). También sugirió probar primero con ODBC Driver 18 y, ante problemas de certificado, ajustar la conexión o usar el Driver 17.

Undecimo Prompt -  Corrección para respetar `esquema.py`
Analizando la propuesta, noto una falla importante en el desacoplamiento: el script `pipeline.py` está haciendo consultas SQL directas con nombres físicos de tablas y columnas en español/inglés directamente hardcodeados.
En las actividades anteriores definimos un archivo de configuración llamado `esquema.py` que contiene un diccionario con el mapeo de la base de datos y la función `renderizar_sql()`.
Reescribir el pipeline para que todas las consultas SQL utilicen las claves canónicas entre llaves (ej: `{{customer}}`, `{{rental.rental_date}}`) e interpolen las tablas/campos reales mediante `renderizar_sql()`.
Generar el script Python para el CSV ficticio complementario (`perfil_comercial_clientes.csv`), que se relacione correctamente con la clave de cliente (`customer_id`).
Incluir *logs* explícitos paso a paso que muestren qué consulta renderizada se está ejecutando en cada etapa.
reconoció la observación y reescribió las consultas como plantillas con claves canónicas, sumó una tabla comparativa entre la versión hardcodeada y la adaptada, y generó `generar_csv.py`, un script que crea `perfil_comercial_clientes.csv` con IDs alineados a la base (600 clientes, datos ficticios y semilla fija). También propuso una estructura de carpetas.

Duodecimo prompt - en los hallazgos del notebook y el informe que datos estan mas cerca a la grafica.
para que: decidir que la consigna se cumple y los graficos estan correctos.

Decimotercero prompt - pruebas de ejecucion para verificar.
para que: que este funcionando todo lo que se fue realizando en segmentos.