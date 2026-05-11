<div align="center">

# Proyecto 3: Motor de Inferencia Simbólica

## **Introducción a la Inteligencia Artificial — Pontificia Universidad Javeriana**

![Logo de la Pontificia Universidad Javeriana](https://upload.wikimedia.org/wikipedia/commons/6/6c/Javeriana.svg)

**Autores:** Juan Daniel Ortiz - Nicolas Castañeda - Juan David Rincon - Nicolás Torres  
**Entregado a:** Ing. Julio Omar Palacio Niño  
**Fecha de entrega:** 10 de Mayo 2026

<br>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![JSON](https://img.shields.io/badge/KB-64%20reglas-1A6B61?style=flat-square)](./base_conocimiento.json)
[![Dominio](https://img.shields.io/badge/Dominio-M%C3%A9dico-E0F2EF?style=flat-square&color=1A6B61)](./base_conocimiento.json)
[![License](https://img.shields.io/badge/Licencia-Académica-lightgrey?style=flat-square)](.)

</div>

---

## Tabla de Contenidos

1. [Descripción del proyecto](#-descripción-del-proyecto)
2. [Estructura del repositorio](#-estructura-del-repositorio)
3. [Fundamento teórico](#-fundamento-teórico)
4. [Base de Conocimiento](#-base-de-conocimiento)
5. [Implementación](#-implementación)
6. [Cómo ejecutar](#-cómo-ejecutar)
7. [Casos de prueba](#-casos-de-prueba)
8. [Interfaz de validación](#-interfaz-de-validación)

---

## Descripción del proyecto

Este proyecto implementa un **Motor de Inferencia de Propósito General** basado en el algoritmo de **Encadenamiento hacia Adelante (Forward Chaining)**, aplicado a un dominio de diagnóstico médico.

El sistema resuelve el problema de la **consecuencia lógica** `KB ⊨ α`:

| Componente | Descripción |
|---|---|
| **KB** | Base de Conocimiento con reglas de la forma `P₁ ∧ P₂ ∧ … ∧ Pₙ → Q` (Cláusulas de Horn) |
| **△ (Hechos)** | Conjunto de síntomas iniciales observados en el paciente |
| **α (Objetivo)** | Diagnóstico o hipótesis médica a verificar |

El motor determina si `α` se deriva lógicamente de `△` aplicando las reglas de la `KB`.

---

## Estructura del repositorio

```
Proyecto3-motorInferencia/
│
├── base_conocimiento.json     # Base de Conocimiento (64 reglas, 8 dominios)
├── motor_inferencia.html      # Interfaz web de validación interactiva
├── proyecto_inferencia.py     # Motor de inferencia (Forward Chaining)
└── README.md
```

---

## Fundamento Teórico

### Cláusulas de Horn

Todas las reglas de la KB siguen la forma de **Cláusula de Horn definida**:

```
P₁ ∧ P₂ ∧ … ∧ Pₙ  →  Q
```

Donde los antecedentes `Pᵢ` son síntomas u hechos intermedios ya conocidos, y el consecuente `Q` es el único hecho positivo que se infiere.

### Algoritmo de Encadenamiento hacia Adelante

El algoritmo opera sobre el principio del **Punto Fijo**: itera sobre todas las reglas de la KB hasta que no sea posible derivar ningún hecho nuevo, o hasta encontrar el objetivo `α`.

```
INICIO
  Cargar síntomas en Memoria de Trabajo M
  MIENTRAS hubo_cambios:
    hubo_cambios ← False
    PARA CADA regla R en KB:
      SI antecedentes(R) ⊆ M  Y  consecuente(R) ∉ M:
        M ← M ∪ { consecuente(R) }
        hubo_cambios ← True
        SI consecuente(R) == α → retornar VERDADERO
  retornar FALSO   ← punto fijo sin objetivo
FIN
```

### Restricciones de la KB

| Restricción | Descripción |
|---|---|
| **Horn** | Solo antecedentes con `AND`, un único consecuente positivo |
| **Aciclicidad** | Sin ciclos `A → B → A`; garantiza terminación |
| **Alcanzabilidad** | Toda regla puede activarse desde síntomas observables |
| **Interdependencia** | Existen hechos intermedios que encadenan síntomas con diagnósticos |

---

## Base de Conocimiento

La KB se almacena externamente en `base_conocimiento.json` para garantizar la **modularidad** del sistema: el motor puede razonar sobre cualquier dominio sin modificar el código.

### Formato

```json
{
  "reglas": [
    {
      "id": "R01",
      "antecedentes": ["Fiebre", "Tos"],
      "consecuente": "Infeccion_Respiratoria"
    },
    {
      "id": "R02",
      "antecedentes": ["Infeccion_Respiratoria", "Dificultad_Respiratoria"],
      "consecuente": "Neumonia"
    }
  ]
}
```

### Estadísticas

| Métrica | Valor |
|---|---|
| Total de reglas | **64** |
| Síntomas primarios | 30 |
| Hechos intermedios | 17 |
| Diagnósticos finales | 17 |
| Dominios cubiertos | 8 |
| Longitud máxima de cadena | 4 pasos |

### Dominios cubiertos

| Dominio | Diagnósticos |
|---|---|
| Respiratorio | Neumonía, Neumonía Bacteriana, Pleuritis |
| Viral sistémico | Gripe, COVID-19, Varicela, Chikungunya |
| Arboviral | Dengue, Dengue Severo, Dengue Hemorrágico |
| Crónico-pulmonar | Tuberculosis, Tuberculosis Avanzada |
| Hepatológico | Hepatitis A, Hepatitis B, Hepatitis B Crónica |
| Neurológico | Meningitis Viral, Meningitis Bacteriana |
| Gastrointestinal | Gastroenteritis, Apendicitis, Intoxicación Alimentaria |
| Cardiovascular | Arritmia, Insuficiencia Cardíaca, Sepsis |

---

## Implementación

### Clases principales

**`Regla`** — representa una regla de la KB:

```python
class Regla:
    def __init__(self, id_regla, antecedentes, consecuente):
        self.id_regla     = id_regla
        self.antecedentes = set(antecedentes)
        self.consecuente  = consecuente
```

**`MotorInferencia`** — carga la KB y ejecuta el razonamiento:

```python
class MotorInferencia:
    def __init__(self, ruta_kb):
        self.reglas          = self.cargar_kb(ruta_kb)
        self.memoria_trabajo = set()
        self.traza           = []
```

### Función `ejecutar_inferencia()`

```python
def ejecutar_inferencia(self, hechos_iniciales, objetivo):
    self.memoria_trabajo = set(hechos_iniciales)
    self.traza = []
    hubo_cambios = True
    iteracion = 0

    while hubo_cambios:
        hubo_cambios = False
        iteracion += 1

        for regla in self.reglas:
            if regla.antecedentes.issubset(self.memoria_trabajo):
                if regla.consecuente not in self.memoria_trabajo:
                    self.memoria_trabajo.add(regla.consecuente)
                    hubo_cambios = True
                    self.traza.append({
                        "iteracion":    iteracion,
                        "regla":        regla.id_regla,
                        "antecedentes": list(regla.antecedentes),
                        "consecuente":  regla.consecuente
                    })
                    if regla.consecuente == objetivo:
                        return True
    return False
```

### Complejidad

| Aspecto | Complejidad |
|---|---|
| Tiempo (peor caso) | `O(n · m · k)` — n reglas × m iteraciones × k antecedentes |
| Espacio | `O(f)` — f hechos únicos en la KB |
| Verificación `issubset()` | `O(k)` con hashing |
| Convergencia | Garantizada por la aciclicidad de la KB |

---

## Cómo ejecutar

**Requisitos:** Python 3.8 o superior. No se requieren dependencias externas.

```bash
# 1. Clonar o descargar el repositorio
# 2. Asegurarse de que proyecto_inferencia.py y base_conocimiento.json están en la misma carpeta

# 3. Ejecutar el motor con los casos de prueba incluidos
python proyecto_inferencia.py
```

Para usar el motor desde otro script:

```python
from proyecto_inferencia import MotorInferencia

motor = MotorInferencia("base_conocimiento.json")

sintomas  = ["Fiebre", "Tos", "Dificultad_Respiratoria"]
hipotesis = "Neumonia"

resultado = motor.ejecutar_inferencia(sintomas, hipotesis)

print(f"KB |= {hipotesis}? → {resultado}")
motor.imprimir_traza()
```

---

## Casos de prueba

### Caso 1 — Neumonía (cadena de 2 pasos)

```
Síntomas : ["Fiebre", "Tos", "Dificultad_Respiratoria"]
Objetivo : "Neumonia"

KB |= Neumonia? → True

Traza:
  [1] R01: Fiebre AND Tos => Infeccion_Respiratoria
  [1] R02: Dificultad_Respiratoria AND Infeccion_Respiratoria => Neumonia
```

### Caso 2 — COVID-19 (cadena de 3 pasos)

```
Síntomas : ["Fiebre", "Perdida_Olfato", "Perdida_Gusto", "Dificultad_Respiratoria", "Fatiga"]
Objetivo : "COVID19"

KB |= COVID19? → True

Traza:
  [1] R09: Fiebre AND Perdida_Gusto AND Perdida_Olfato => Infeccion_Viral_Respiratoria
  [1] R10: Dificultad_Respiratoria AND Infeccion_Viral_Respiratoria => COVID19_Probable
  [1] R11: COVID19_Probable AND Fatiga => COVID19
```

### Caso 3 — Punto fijo sin objetivo

```
Síntomas : ["Congestion_Nasal", "Dolor_Garganta"]
Objetivo : "Tuberculosis"

KB |= Tuberculosis? → False

Traza: (No se activó ninguna regla)
```

---

## Interfaz de Validación

El archivo `motor_inferencia.html` es una interfaz web interactiva que replica el motor completo en el navegador, pensada para demostración en clase.

**Cómo usar:**

1. Abrir `motor_inferencia.html` en el navegador
2. Arrastrar o seleccionar el archivo `base_conocimiento.json`
3. Seleccionar síntomas del panel izquierdo
4. Elegir un diagnóstico objetivo y presionar **Ejecutar KB ⊨ α**

La interfaz muestra el veredicto (`KB ⊨ α` o `KB ⊭ α`), la traza de razonamiento paso a paso con el ID de cada regla activada, y la memoria de trabajo final diferenciando síntomas iniciales de hechos inferidos.
 
---

<div align="center">

**Pontificia Universidad Javeriana - Facultad de Ingeniería**

</div>