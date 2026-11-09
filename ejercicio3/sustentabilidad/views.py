from django.shortcuts import render

from .metricas import obtener_metricas_consumo

# Historial de consumos de ejemplo (en un caso real vendría de una base de datos)
REGISTROS_CONSUMO = [
    {"planta": "Planta Norte", "consumo_kwh": 1200},
    {"planta": "Planta Sur", "consumo_kwh": 850.5},
    {"planta": "Planta Este", "consumo_kwh": 430},
    {"planta": "Planta Norte", "consumo_kwh": 300},
]


def vista_panel_sustentabilidad(request):
    """Calcula las métricas y renderiza sustentabilidad/panel.html con el contexto."""
    metricas = obtener_metricas_consumo(REGISTROS_CONSUMO)
    contexto = {
        "titulo": "Panel de Sustentabilidad - EcoTech Solutions",
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "consumo_mayor_kwh": metricas["consumo_mayor_kwh"],
        "detalle_plantas": metricas["detalle_plantas"],
    }
    return render(request, "sustentabilidad/panel.html", contexto)

