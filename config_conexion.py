import urllib.parse
from sqlalchemy import create_engine

#Configuracion de servidor segun tus datos de SSMS
SERVIDOR = r".\SQLEXPRESS"
BASE_DATOS = "sakila"


#Construccion segura de la cadena de conexion codificada
connection_string   = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVIDOR};"
    f"DATABASE={BASE_DATOS};"
    f"Trusted_Connection=yes;"
    f"Encrypt=no;"
    f"TrustedServerCertificate=yes;"
)

params=urllib.parse.quote_plus(connection_string)
# Cadena de conexión usando Autenticación Integrada de Windows
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"


# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)


def probar_conexion():
    """Verifica que la conexión a SQL Server sea exitosa."""
    try:
        with engine.connect() as conn:
            print("¡Conexión a SQL Server exitosa!")
            return True

    except Exception as e:
        print(f"Error de conexión: {e}")
        return False


if __name__ == "__main__":
    probar_conexion()
