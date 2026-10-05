import os
import urllib.parse
from sqlalchemy import create_engine

# Configuración local. Cada integrante puede sobreescribir estos valores sin
# modificar el código mediante SQL_SERVER, SQL_DATABASE y SQL_ODBC_DRIVER.
# No se guardan credenciales: se usa la autenticación integrada de Windows.
SERVIDOR = os.getenv("SQL_SERVER", r".\SQLEXPRESS")
BASE_DATOS = os.getenv("SQL_DATABASE", "sakila")
CONTROLADOR = os.getenv("SQL_ODBC_DRIVER", "ODBC Driver 18 for SQL Server")


#Construccion segura de la cadena de conexion codificada
connection_string = (
    f"DRIVER={{{CONTROLADOR}}};"
    f"SERVER={SERVIDOR};"
    f"DATABASE={BASE_DATOS};"
    f"Trusted_Connection=yes;"
    f"Encrypt=no;"
    f"TrustedServerCertificate=yes;"
)

params = urllib.parse.quote_plus(connection_string)
# Cadena de conexión usando Autenticación Integrada de Windows
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"


# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def probar_conexion():
    """Verifica que la conexión a SQL Server sea exitosa."""
    try:
        with engine.connect() as conn:
            print("¡Conexión a SQL Server exitosa!")
            return True

    except Exception as error:
        print(f"Error de conexión: {error}")
        return False


if __name__ == "__main__":
    probar_conexion()
