import unittest
from unittest.mock import patch

import esquema
from reconciliar_origen import contar_origen, contar_tuplas


class ConteoOrigenTest(unittest.TestCase):
    def test_cadenas_y_parentesis_no_crean_filas(self):
        sql = "(1, 'texto (con), signos; y comilla ''simple''', FUNCION(1, 2)), (3, 'otro');"
        self.assertEqual(contar_tuplas(sql, 0), (2, [1, 3]))

    def test_sentencia_incompleta_no_se_acepta(self):
        with self.assertRaises(ValueError):
            contar_tuplas("(1, 'sin cierre')", 0)

    def test_archivo_aportado_por_el_equipo(self):
        origen = contar_origen()
        self.assertEqual(len(origen["conteos"]), 16)
        self.assertEqual(origen["pagos"]["filas"], 16044)
        self.assertEqual(origen["pagos"]["max_id"], 16049)
        self.assertEqual(origen["pagos"]["huecos_id"], [424, 7011, 10840, 14675, 15458])
        self.assertIn("trigger", origen["metodos"]["film_text"])


class PortabilidadTest(unittest.TestCase):
    def test_mapeo_destino_no_cambia_el_conteo_historico(self):
        with patch.dict(esquema.MAPEO_TABLAS, {"customer": "ClientesEquipoB", "film": "PeliculasEquipoB"}):
            origen = contar_origen()
        self.assertEqual(origen["conteos"]["customer"], 599)
        self.assertEqual(origen["conteos"]["film_text"], 1000)

    def test_cambiar_solo_el_mapeo_cambia_el_sql(self):
        with patch.dict(esquema.MAPEO_TABLAS, {"customer": "ClientesEquipoB"}), patch.dict(
            esquema.MAPEO_COLUMNAS["customer"], {"customer_id": "ClienteID"}
        ):
            sql = esquema.renderizar_sql("SELECT {{customer.customer_id}} FROM {{customer}}")
        self.assertEqual(sql, "SELECT [ClienteID] FROM [dbo].[ClientesEquipoB]")

    def test_token_desconocido_o_invalido_falla(self):
        with self.assertRaises(KeyError):
            esquema.renderizar_sql("SELECT {{customer.no_existe}} FROM {{customer}}")
        with self.assertRaises(ValueError):
            esquema.renderizar_sql("SELECT {{customer.123}}")


if __name__ == "__main__":
    unittest.main()
