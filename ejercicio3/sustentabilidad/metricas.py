"""Lógica pura (sin dependencias de Django) de cálculo de emisiones y métricas."""


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Calcula las emisiones de CO2 (kg) = consumo_kwh * factor_emision.

    Lanza ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """Procesa el historial de consumos por planta industrial.

    registros: lista de dicts {"planta": str, "consumo_kwh": número}. Una planta puede
    aparecer varias veces (historial); sus consumos se acumulan.

    Devuelve un dict con:
      - total_emisiones: emisiones globales (kg CO2)
      - planta_mayor_consumo: nombre de la planta con mayor consumo total (None si no hay datos)
      - consumo_mayor_kwh: consumo total de esa planta
      - detalle_plantas: lista de {"planta", "consumo_kwh", "emisiones"}
    """
    consumo_por_planta = {}
    for registro in registros:
        planta = registro["planta"]
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0) + registro["consumo_kwh"]

    detalle = [
        {
            "planta": planta,
            "consumo_kwh": consumo,
            "emisiones": calcular_emisiones_carbono(consumo),
        }
        for planta, consumo in consumo_por_planta.items()
    ]

    total_emisiones = sum(d["emisiones"] for d in detalle)
    if detalle:
        mayor = max(detalle, key=lambda d: d["consumo_kwh"])
        planta_mayor, consumo_mayor = mayor["planta"], mayor["consumo_kwh"]
    else:
        planta_mayor, consumo_mayor = None, 0

    return {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor,
        "consumo_mayor_kwh": consumo_mayor,
        "detalle_plantas": detalle,
    }

