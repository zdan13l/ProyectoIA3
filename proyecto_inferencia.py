import json

# ==========================================================
# PARTE 1: ESTRUCTURA DE DATOS (NO MODIFICAR)
# ==========================================================
class Regla:
    def __init__(self, id_regla, antecedentes, consecuente):
        self.id_regla = id_regla
        self.antecedentes = set(antecedentes)
        self.consecuente = consecuente

    def __str__(self):
        return f"{self.id_regla}: {' AND '.join(self.antecedentes)} -> {self.consecuente}"

class MotorInferencia:
    def __init__(self, ruta_kb):
        self.reglas = self.cargar_kb(ruta_kb)
        self.memoria_trabajo = set()

        # Registro de reglas activadas (Traza de Explicación).
        self.traza = []

    def cargar_kb(self, ruta):
        """Carga las reglas desde un archivo JSON."""
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return [Regla(r.get('id'), r['antecedentes'], r['consecuente']) for r in datos['reglas']]
        except Exception as e:
            print(f"Error al cargar la Base de Conocimiento: {e}")
            return []


    # ==========================================================
    # PARTE 2: ALGORITMO DE ENCADENAMIENTO HACIA ADELANTE
    # ==========================================================
    def ejecutar_inferencia(self, hechos_iniciales, objetivo):
        """
        Implementa el algoritmo de Encadenamiento hacia Adelante (Forward Chaining).

        El  algoritmo busca el 'Punto Fijo':  itera sobre todas las reglas de la  KB
        hasta  que ya no se puedan  derivar nuevos hechos.  Si en  algún  momento se
        infiere el objetivo, retorna True de inmediato.

        Entradas:
        - hechos_iniciales: Lista de síntomas (ejemplo. ["Fiebre", "Tos"])
        - objetivo: El diagnóstico a verificar (ejemplo. "Neumonia")

        Retorna:
        - True si el objetivo es consecuencia lógica (KB |= objetivo).
        - False si se alcanza un punto fijo sin hallar el objetivo.
        """

        # 1. INICIALIZACIÓN: cargar hechos iniciales en la Memoria de Trabajo.
        self.memoria_trabajo = set(hechos_iniciales)
        self.traza = []
        hubo_cambios = True

        # 2. CICLO DE INFERENCIA (búsqueda del Punto Fijo).
        iteracion = 0
        while hubo_cambios:
            hubo_cambios = False
            iteracion += 1

            # Recorrer cada regla de la KB.
            for regla in self.reglas:

                # Verificar si los antecedentes son subconjunto de la memoria de trabajo.
                if regla.antecedentes.issubset(self.memoria_trabajo):

                    # Solo actuar si el consecuente aún no es conocido.
                    if regla.consecuente not in self.memoria_trabajo:

                        # Agregar el nuevo hecho inferido
                        self.memoria_trabajo.add(regla.consecuente)
                        # Hubo cambio: continuar el ciclo.
                        hubo_cambios = True

                        # Registrar en la Traza de Explicación.
                        self.traza.append({
                            "iteracion": iteracion,
                            "regla": regla.id_regla,
                            "antecedentes": list(regla.antecedentes),
                            "consecuente": regla.consecuente
                        })

                        # 3. CONDICIÓN DE ÉXITO: se encontró el objetivo.
                        if regla.consecuente == objetivo:
                            return True

        # 4. CONDICIÓN DE PARADA: se alcanzó el punto fijo sin hallar el objetivo.
        return False

    # Función adicional para imprimir la traza de razonamiento.
    def imprimir_traza(self):
        """Imprime la cadena de razonamiento que llevó al diagnóstico."""
        if not self.traza:
            print("  (No se activó ninguna regla)")
            return
        for paso in self.traza:
            antecedentes_str = " AND ".join(sorted(paso["antecedentes"]))
            print(f"  [{paso['iteracion']}] {paso['regla']}: "
            f"{antecedentes_str} => {paso['consecuente']}")


# ==========================================================
# PARTE 3: EJECUCIÓN (PUEDEN MODIFICAR PARA PRUEBAS)
# ==========================================================
if __name__ == "__main__":
    # 1. Inicializar el motor con el archivo de reglas.
    motor = MotorInferencia("base_conocimiento.json")
    print(f"Base de Conocimiento cargada: {len(motor.reglas)} reglas.\n")

    # -------------------------------------------------------
    # CASO 1: Neumonía (cadena de 2 pasos).
    # -------------------------------------------------------
    sintomas   = ["Fiebre", "Tos", "Dificultad_Respiratoria"]
    hipotesis  = "Neumonia"

    print("=" * 50)
    print(f"CASO 1")
    print(f"  Síntomas : {sintomas}")
    print(f"  Objetivo : {hipotesis}")

    resultado = motor.ejecutar_inferencia(sintomas, hipotesis)

    print(f"  ¿KB |= {hipotesis}? -> {resultado}")
    print("  Traza de razonamiento:")
    motor.imprimir_traza()

    # -------------------------------------------------------
    # CASO 2: COVID-19 (cadena de 3 pasos).
    # -------------------------------------------------------
    sintomas2  = ["Fiebre", "Perdida_Olfato", "Perdida_Gusto", "Dificultad_Respiratoria", "Fatiga"]
    hipotesis2 = "COVID19"

    print("\n" + "=" * 50)
    print(f"CASO 2")
    print(f"  Síntomas : {sintomas2}")
    print(f"  Objetivo : {hipotesis2}")

    resultado2 = motor.ejecutar_inferencia(sintomas2, hipotesis2)

    print(f"  ¿KB |= {hipotesis2}? -> {resultado2}")
    print("  Traza de razonamiento:")
    motor.imprimir_traza()

    # -------------------------------------------------------
    # CASO 3: Objetivo inalcanzable (punto fijo sin éxito).
    # -------------------------------------------------------
    sintomas3  = ["Congestion_Nasal", "Dolor_Garganta"]
    hipotesis3 = "Tuberculosis"

    print("\n" + "=" * 50)
    print(f"CASO 3")
    print(f"  Síntomas : {sintomas3}")
    print(f"  Objetivo : {hipotesis3}")

    resultado3 = motor.ejecutar_inferencia(sintomas3, hipotesis3)

    print(f"  ¿KB |= {hipotesis3}? -> {resultado3}")
    print("  Traza de razonamiento:")
    motor.imprimir_traza()
    print("=" * 50)
