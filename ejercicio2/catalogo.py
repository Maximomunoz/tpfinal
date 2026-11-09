"""Ejercicio 2 - Modelo de productos, excepciones y persistencia (EcoTech Solutions)."""

import json


class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock inválido (negativo o no entero)."""


class DispositivoEcologico:
    """Clase base de los productos ecológicos del catálogo."""

    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock  # pasa por el setter y se valida

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError(f"El stock debe ser un entero, se recibió: {valor!r}")
        if valor < 0:
            raise StockInvalidoError(f"El stock no puede ser negativo: {valor}")
        self._stock = valor

    def ficha_tecnica(self):
        return f"{self.nombre} | Precio: ${self.precio:,.2f} | Stock: {self.stock} unidades"

    def to_dict(self):
        return {
            "tipo": type(self).__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


# Alias con el nombre escrito como en la consigna (con tilde)
DispositivoEcológico = DispositivoEcologico


class PanelSolar(DispositivoEcologico):
    """Panel solar: agrega potencia y eficiencia, y personaliza la ficha técnica."""

    def __init__(self, nombre, precio, stock, potencia_watts, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia  # porcentaje, ej. 21.5

    def ficha_tecnica(self):
        return (
            f"[PANEL SOLAR] {self.nombre}\n"
            f"  Potencia  : {self.potencia_watts} W\n"
            f"  Eficiencia: {self.eficiencia}%\n"
            f"  Precio    : ${self.precio:,.2f}\n"
            f"  Stock     : {self.stock} unidades"
        )

    def to_dict(self):
        datos = super().to_dict()
        datos.update({"potencia_watts": self.potencia_watts, "eficiencia": self.eficiencia})
        return datos


class GestorInventario:
    """Gestiona la persistencia del catálogo."""

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo="catalogo_ecotech.json"):
        datos = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        return ruta_archivo


if __name__ == "__main__":
    catalogo = []

    # Productos válidos
    catalogo.append(DispositivoEcologico("Cargador solar portátil", 45.5, 30))
    catalogo.append(PanelSolar("Panel Solar EcoMax 450W", 320.0, 12, 450, 21.5))

    # Intentos con stock inválido: se capturan de forma controlada
    intentos = [
        lambda: PanelSolar("Panel Defectuoso", 100.0, -5, 300, 18.0),
        lambda: setattr(catalogo[0], "stock", -1),
    ]
    for intento in intentos:
        try:
            intento()
        except StockInvalidoError as error:
            print(f"[StockInvalidoError capturado] {error}")

    print("\n--- Fichas técnicas ---")
    for dispositivo in catalogo:
        print(dispositivo.ficha_tecnica())
        print()

    ruta = GestorInventario().guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Catálogo exportado correctamente a '{ruta}' ({len(catalogo)} productos).")

