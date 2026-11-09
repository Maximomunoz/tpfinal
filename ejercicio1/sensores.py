"""Ejercicio 1 - Sanitización y análisis estadístico de sensores (EcoTech Solutions)."""

import re

UBICACION_POR_DEFECTO = "Sin ubicación"
_PATRON_NUMERO = re.compile(r"[-+]?\d+(?:[.,]\d+)?")


def _limpiar_temperatura(valor):
    """Convierte '24.5C', ' 24,5 °C ', 24 o 24.5 a float. Lanza ValueError si no hay número."""
    if isinstance(valor, bool):
        raise ValueError(f"Temperatura inválida: {valor!r}")
    if isinstance(valor, (int, float)):
        return float(valor)
    coincidencia = _PATRON_NUMERO.search(str(valor))
    if coincidencia is None:
        raise ValueError(f"Temperatura inválida: {valor!r}")
    return float(coincidencia.group().replace(",", "."))


def limpiar_registro_sensor(registro_raw):
    """Normaliza un registro crudo de sensor y devuelve un nuevo diccionario estandarizado.

    - sensor_id: sin espacios sobrantes.
    - temperatura: float sin sufijos de unidad.
    - ubicacion: sin espacios; si falta o está vacía se usa un valor por defecto.
    """
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()
    if not sensor_id:
        raise ValueError("El registro no tiene 'sensor_id'")

    if registro_raw.get("temperatura") is None:
        raise ValueError(f"El sensor {sensor_id} no tiene 'temperatura'")
    temperatura = _limpiar_temperatura(registro_raw["temperatura"])

    ubicacion = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion).strip() if ubicacion is not None else ""
    if not ubicacion:
        ubicacion = UBICACION_POR_DEFECTO

    return {"sensor_id": sensor_id, "temperatura": temperatura, "ubicacion": ubicacion}


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """Devuelve (lista_sensores_alerta, promedio_temperatura).

    lista_sensores_alerta: IDs de sensores con temperatura estrictamente mayor al umbral.
    promedio_temperatura: promedio global (0.0 si la lista está vacía).
    """
    if not lista_sensores_limpios:
        return [], 0.0

    alertas = [s["sensor_id"] for s in lista_sensores_limpios if s["temperatura"] > umbral_temperatura]
    promedio = sum(s["temperatura"] for s in lista_sensores_limpios) / len(lista_sensores_limpios)
    return alertas, promedio


if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.2 °C ", "ubicacion": "  Planta Sur "},
        {"sensor_id": "  SENSOR-003", "temperatura": "38C"},
        {"sensor_id": "SENSOR-004 ", "temperatura": "27,8C", "ubicacion": ""},
        {"sensor_id": "SENSOR-005", "temperatura": "abc", "ubicacion": "Planta Este"},  # inválido
    ]
    UMBRAL = 30.0

    sensores_limpios = []
    for crudo in registros_crudos:
        try:
            sensores_limpios.append(limpiar_registro_sensor(crudo))
        except ValueError as error:
            print(f"[AVISO] Registro descartado: {error}")

    alertas, promedio = generar_resumen_sensores(sensores_limpios, UMBRAL)

    print("=" * 50)
    print("REPORTE DE SENSORES - ECOTECH SOLUTIONS")
    print("=" * 50)
    for s in sensores_limpios:
        print(f"{s['sensor_id']:<12} {s['temperatura']:>6.1f} °C  {s['ubicacion']}")
    print("-" * 50)
    print(f"Umbral de temperatura : {UMBRAL:.1f} °C")
    print(f"Sensores en alerta    : {', '.join(alertas) if alertas else 'Ninguno'}")
    print(f"Promedio global       : {promedio:.2f} °C")

