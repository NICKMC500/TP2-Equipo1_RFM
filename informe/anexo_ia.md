# Anexo de trazabilidad del uso de IA

## 1. Bitácora de prompts

Durante el desarrollo del proyecto utilizamos una herramienta de inteligencia artificial para analizar errores, revisar el código y proponer modificaciones. A continuación, registramos las principales consultas realizadas y el objetivo de cada una.

### Primer prompt: error de sintaxis en SQL Server

**Error informado:**

`ProgrammingError: ('42000', "[Microsoft][ODBC Driver 18 for SQL Server][SQL Server]Incorrect syntax near 'go'. (102)...")`

El error apareció al intentar ejecutar `conjunto_trabajo.sql` desde Python.

**Objetivo:** identificar por qué SQL Server rechazaba el archivo SQL al ejecutarlo mediante SQLAlchemy.

### Segundo prompt: error al calcular quintiles

**Error informado:**

`ValueError: Bin edges must be unique`

El mensaje mostraba bordes repetidos al intentar dividir los valores de recencia en quintiles.

**Objetivo:** comprender por qué fallaba `pd.qcut`. La presencia de numerosos valores repetidos dificultaba la división en cinco grupos con límites únicos.

### Tercer prompt: nombre de columna incorrecto

**Error informado:**

`KeyError: 'cliente_id'`

El error apareció al realizar la verificación de duplicados y el resumen del DataFrame.

**Objetivo:** corregir la diferencia entre el nombre de columna utilizado en el código (`cliente_id`) y el nombre físico de la columna en la base de datos (`id_cliente`).

### Cuarto prompt: revisión del análisis IQR

Solicitamos revisar la celda 4 del notebook, correspondiente al análisis de valores atípicos mediante el rango intercuartílico (IQR). La consulta incluía el cálculo de los cuartiles de `monto_total` y la comprobación de reglas de negocio, como la cantidad de registros con frecuencia menor o igual a cero.

**Objetivo:** validar el análisis de valores atípicos y comprobar la aplicación de las reglas de negocio.

### Quinto prompt: variable no definida

**Error informado:**

`NameError: name 'df_rfm' is not defined`

El error apareció después de reiniciar el kernel del notebook.

**Objetivo:** comprender por qué la variable ya no estaba disponible y cómo recuperar la ejecución correcta.

### Sexto prompt: validación de resultados del análisis IQR

Compartimos la salida obtenida en la celda 4:

- Q1: 94,78.
- Q3: 128,70.
- IQR: 33,92.
- Violaciones por monto negativo: 0.
- Violaciones por frecuencia menor o igual a cero: 0.

**Objetivo:** comprobar que los resultados obtenidos fueran coherentes con el análisis implementado.

### Séptimo prompt: revisión de errores y recencia

Informamos que la actividad 1 presentaba errores de ejecución. Durante la revisión aparecieron nuevamente problemas relacionados con `NameError` y diferencias entre la recencia calculada en SQL Server y en pandas.

**Objetivo:** identificar la causa de las diferencias y corregir la validación entre ambas implementaciones.

### Octavo prompt: traducción de las salidas del notebook

Solicitamos que las salidas del notebook estuvieran en español y señalamos que todavía aparecían términos en inglés, como `count`, `mean`, `min`, `RangeIndex`, `Non-Null Count`, `dtype` y `memory usage`.

**Objetivo:** mejorar la claridad de los resultados para que fueran comprensibles y consistentes con el idioma utilizado en el proyecto.

### Noveno prompt: revisión final antes de publicar

Solicitamos una última revisión del proyecto antes de realizar el `commit` y el `push` a la rama `main`.

**Objetivo:** detectar posibles inconvenientes pendientes y comprobar el estado general del trabajo antes de publicarlo en el repositorio.

### Décimo prompt: diseño del pipeline

Solicitamos diseñar un script Python para:

- Extraer información de clientes y transacciones desde SQL Server.
- Leer el archivo complementario `perfil_comercial_clientes.csv`.
- Combinar y transformar los datos para calcular las métricas RFM.
- Cargar los resultados en una tabla de destino de SQL Server.
- Garantizar la idempotencia del proceso.
- Revisar el estado del repositorio y el `README.md` para adaptar la propuesta a la estructura existente.

**Resultado de la consulta:** la herramienta propuso una estructura de pipeline en cuatro etapas: extracción, transformación, carga y orquestación. También sugirió realizar la carga mediante `DELETE` e `INSERT` dentro de una transacción, incorporar manejo de excepciones y logging, y revisar la configuración del controlador ODBC.

Estas propuestas debían contrastarse con la implementación real del proyecto antes de considerarlas definitivas.

### Undécimo prompt: corrección del uso de `esquema.py`

Al revisar la propuesta del pipeline, detectamos que las consultas utilizaban nombres físicos de tablas y columnas directamente en el código, en lugar de resolverlos mediante el mecanismo de equivalencias definido en `esquema.py`.

Solicitamos que todas las consultas utilizaran nombres canónicos mediante tokens, por ejemplo `{{customer}}` y `{{rental.rental_date}}`, y que las tablas y columnas físicas se obtuvieran mediante `renderizar_sql()`.

También solicitamos que el archivo complementario `perfil_comercial_clientes.csv` se relacionara correctamente mediante la clave canónica `customer_id`, que se incorporaran registros de logging y que se mostraran las consultas renderizadas durante las distintas etapas.

**Resultado de la consulta:** la herramienta propuso adaptar las consultas para utilizar plantillas con nombres canónicos, explicó las diferencias respecto de la versión anterior y generó una propuesta para crear un CSV ficticio con identificadores alineados con los clientes de la base.

### Duodécimo prompt: relación entre los hallazgos y los gráficos

Solicitamos revisar los hallazgos del notebook y su relación con los gráficos generados para el informe.

**Objetivo:** comprobar que las conclusiones estuvieran respaldadas por los resultados y que los gráficos fueran adecuados para comunicar los hallazgos.

### Decimotercer prompt: pruebas de ejecución

Solicitamos realizar pruebas para verificar el funcionamiento de las distintas partes desarrolladas.

**Objetivo:** comprobar que las actividades y los componentes del proyecto se ejecutaran correctamente después de los cambios realizados.

---

## 2. Correcciones manuales y participación del equipo

La herramienta de IA propuso y aplicó gran parte de las correcciones al código a partir de los errores y las consultas que le enviamos. Nuestra intervención consistió en supervisar el proceso y verificar los resultados.

Las principales acciones realizadas fueron:

- Detectamos errores durante la ejecución del notebook y enviamos los mensajes de error completos para facilitar su diagnóstico.
- Solicitamos explicaciones antes de aplicar cambios, para comprenderlos y evitar afectar el trabajo de los compañeros.
- Pedimos que la ejecución se realizara en el entorno virtual `venv_tp2`, según lo establecido en la consigna, y que las salidas del notebook estuvieran en español.
- Revisamos los resultados obtenidos, incluidos el análisis IQR y la comparación entre SQL Server y pandas, antes de aceptar las modificaciones.
- Decidimos cuándo realizar el `commit` y el `push` a `main`, después de una revisión final del proyecto.

### Resolución de los principales errores

- **Error de sintaxis cerca de `GO`:** la versión final de `conjunto_trabajo.sql` quedó sin instrucciones `GO`, según la revisión realizada.
- **`Bin edges must be unique`:** se reemplazó el uso directo de `pd.qcut` por la función `puntuar_quintiles`, que ordena los registros por valor e identificador y aplica `rank(method="first")` antes de dividirlos en quintiles.
- **`KeyError: 'cliente_id'`:** se corrigió la resolución de nombres mediante el mapeo centralizado en `esquema.py`.
- **`NameError: name 'df_rfm' is not defined`:** el error apareció después de reiniciar el kernel y se resolvió ejecutando las celdas del notebook desde el principio y en orden.
- **Diferencias en la recencia:** se normalizaron las fechas antes de calcular las diferencias entre ellas para hacer comparables los resultados de SQL Server y pandas.

No tenemos registradas otras correcciones manuales sobre el código generado.

---

## 3. Caso de nombres de tablas o columnas incorrectos

No tenemos registrado un caso comprobado en el que la herramienta haya inventado nombres de tablas o columnas.

El caso más cercano fue el error `KeyError: 'cliente_id'`. Ese nombre no existe en la base de datos del equipo, donde la columna correspondiente se llama `id_cliente`.

No podemos asegurar si el nombre incorrecto fue propuesto por la herramienta o si ya estaba presente en el código inicial. El problema se relacionaba con la diferencia entre los nombres canónicos de Sakila, originalmente en inglés, y los nombres físicos utilizados en la base migrada al español.

La solución consistió en centralizar las equivalencias en `esquema.py`. De esta manera, el código puede utilizar los nombres canónicos y resolverlos según las tablas y columnas reales de la base de datos.

---

## 4. Crítica del código: versión propia frente a versión generada con IA

Comparamos la primera versión del código con la versión modificada mediante IA, prestando atención a la carga del conjunto de trabajo y al cálculo de los quintiles.

### 4.1. Versión propia

```python
with open("../sql/conjunto_trabajo.sql", "r", encoding="utf-8") as f:
    query_rfm = f.read()

df_rfm = pd.read_sql(query_rfm, con=engine)
```

En esta versión, la consulta se leía directamente desde el archivo SQL. Los quintiles se calculaban mediante `pd.qcut` aplicado directamente sobre cada columna.

**Ventajas:**

- Es una implementación corta y fácil de leer.
- Su lógica es sencilla de comprender y depurar.

**Limitaciones:**

- La ruta relativa depende de la ubicación desde la que se ejecuta el código.
- La consulta no resolvía por sí misma las diferencias entre los nombres canónicos y los nombres físicos de la base.
- El cálculo directo mediante `pd.qcut` producía un error cuando los bordes de los intervalos se repetían.

### 4.2. Versión con IA

```python
plantilla_rfm = (
    RAIZ / "sql" / "conjunto_trabajo.sql"
).read_text(encoding="utf-8")

query_rfm = renderizar_sql(plantilla_rfm)
df_rfm = pd.read_sql_query(query_rfm, con=engine)

def puntuar_quintiles(frame, columna, etiquetas):
    ordenado = frame.sort_values(
        [columna, "customer_id"],
        kind="stable"
    )
    rangos = ordenado[columna].rank(method="first")
    puntajes = pd.qcut(
        rangos,
        q=5,
        labels=etiquetas
    ).astype(int)
    ...
```

**Ventajas:**

- Utiliza `esquema.py` y tokens como `{{customer}}` para resolver las tablas y columnas físicas a partir de los nombres canónicos.
- Calcula la raíz del proyecto para construir la ruta al archivo SQL, reduciendo la dependencia de la carpeta desde la que se ejecuta el notebook.
- Resuelve el problema de los valores repetidos al asignar rangos únicos antes de calcular los quintiles.
- Permite detectar tokens sin equivalencia en el mapeo y mostrar un error claro, en lugar de ejecutar una consulta incompleta.

**Limitaciones:**

- La implementación es más compleja y requiere comprender `renderizar_sql()` y el sistema de tokens.
- El desempate mediante el identificador de cliente es una decisión técnica. Dos clientes con el mismo valor pueden quedar en quintiles diferentes.
- La sustitución de tokens debe utilizar nombres procedentes del mapeo controlado del proyecto y no valores arbitrarios de entrada.

### 4.3. Conclusión de la comparación

Decidimos conservar la versión modificada con IA porque permite centralizar la resolución de nombres, reduce la dependencia de la ubicación de ejecución y resuelve el error que se producía al calcular los quintiles con valores repetidos.

Los resultados se compararon con los obtenidos mediante `NTILE(5)` en SQL Server. La comparación registrada indicó una coincidencia del 99,7 %. Este porcentaje debe interpretarse en relación con las puntuaciones que efectivamente se compararon, y no como una garantía de que todos los componentes del análisis sean idénticos.

El desempate utilizado para formar los quintiles constituye una limitación metodológica, ya que los clientes con valores iguales pueden terminar en grupos diferentes.

---

## 5. Conclusiones que los datos no sostenían

Durante la revisión del informe y del notebook identificamos afirmaciones que requerían una formulación más prudente o evidencia adicional.

### 5.1. Diferencia en la cantidad de pagos

En el primer borrador de la sección 2.2 del informe, la herramienta afirmó que se había verificado que la diferencia de cinco pagos entre el volcado original (16.049) y SQL Server (16.044) no afectaba al análisis RFM.

Esa afirmación no estaba respaldada por una comprobación suficiente: los cinco registros no estaban presentes en SQL Server. La diferencia era consistente con la posibilidad de que correspondieran a pagos sin alquiler asociado que no se hubieran migrado, pero eso no demostraba por sí solo que esa fuera la causa ni que la diferencia no afectara al análisis.

Detectamos el problema al contrastar el borrador con la conclusión del notebook, donde se utilizaba una formulación más prudente. Por eso, el informe se corrigió para distinguir entre una explicación posible y un hecho verificado.

### 5.2. Interpretación de los segmentos RFM

En el notebook aparecían los hallazgos «19 clientes con segmento 555» y «120 clientes en el quintil menos reciente». Sin embargo, al preparar el informe, advertimos que esos resultados no estaban acompañados por evidencia gráfica suficiente.

Además, el número aproximado de 120 clientes se explicaba por la distribución de 599 registros en cinco grupos, no por un hallazgo comercial independiente sobre el comportamiento de esos clientes.

Por ello, el tamaño del quintil no debe presentarse como prueba de que esos clientes se están enfriando. Para sostener esa conclusión, es necesario analizar los valores de recencia de los integrantes del grupo, comprobar la orientación de las puntuaciones y relacionarlos con los demás indicadores RFM.

Esta revisión permitió distinguir entre una descripción del resultado de la segmentación y una conclusión comercial respaldada por los datos.