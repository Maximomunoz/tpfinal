import unittest

from django.test import SimpleTestCase

from sustentabilidad.metricas import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """Auditoría de calcular_emisiones_carbono."""

    def test_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(250, 0.5), 125.0)

    def test_consumo_decimal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.5), 5.0)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)

    def test_consumo_negativo_con_factor_personalizado(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50, factor_emision=0.8)

    def test_mensaje_de_error(self):
        with self.assertRaisesRegex(ValueError, "negativo"):
            calcular_emisiones_carbono(-0.01)


class TestObtenerMetricasConsumo(unittest.TestCase):
    def test_total_y_planta_mayor(self):
        registros = [
            {"planta": "Norte", "consumo_kwh": 100},
            {"planta": "Sur", "consumo_kwh": 300},
            {"planta": "Norte", "consumo_kwh": 100},
        ]
        metricas = obtener_metricas_consumo(registros)
        self.assertAlmostEqual(metricas["total_emisiones"], 200.0)
        self.assertEqual(metricas["planta_mayor_consumo"], "Sur")

    def test_sin_registros(self):
        metricas = obtener_metricas_consumo([])
        self.assertEqual(metricas["total_emisiones"], 0)
        self.assertIsNone(metricas["planta_mayor_consumo"])


class TestVistaPanel(SimpleTestCase):
    def test_vista_renderiza_panel(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")
        self.assertIn("planta_mayor_consumo", respuesta.context)
        self.assertEqual(respuesta.context["planta_mayor_consumo"], "Planta Norte")


if __name__ == "__main__":
    unittest.main()
