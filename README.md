# Algoritmos de Primeros, Siguientes y Predicción (LL(1))

Este repositorio contiene la solución completa de la tarea de la asignatura **Lenguajes de Programación y Transducción**, correspondiente al análisis sintáctico descendente LL(1) para dos gramáticas libres de contexto.

---

## 📌 Contenido del Repositorio

- **`grammar_analyzer.py`**: Módulo núcleo en Python con la clase `GrammarAnalyzer`, que implementa:
  - Detección de símbolos anulables ($\alpha \Rightarrow^* \varepsilon$).
  - Cálculo de $\text{PRIMEROS}(\alpha)$ para cadenas de símbolos.
  - Algoritmo de punto fijo para $\text{PRIMEROS}(A)$ de no terminales.
  - Algoritmo de punto fijo para $\text{SIGUIENTES}(A)$ de no terminales con manejo de $\$$ y propagación de $\varepsilon$.
  - Cálculo del conjunto de $\text{PREDICCIÓN}(A \to \alpha)$ para cada producción.
  - Verificación del criterio LL(1) y reporte de conflictos.
  - Generación de la tabla de análisis predictivo $M[A, a]$.
- **`main.py`**: Script ejecutable que resuelve ambas gramáticas, muestra el paso a paso por iteraciones, imprime tablas formateadas y genera la comparación 100% verificada.
- **`test_analyzer.py`**: Suite de pruebas unitarias (`unittest`) que valida la consistencia matemática de los algoritmos contra las deducciones analíticas.
- **`INFORME_TEORICO_Y_COMPARATIVO.md`**: Informe técnico completo con la deducción analítica paso a paso, fundamentación teórica de las diapositivas de clase y tablas comparativas analítico vs. computacional.

---

## 🚀 Requisitos y Ejecución

### Requisitos
- Python 3.8 o superior (no requiere librerías externas, utiliza únicamente la biblioteca estándar).

### Ejecución del programa principal
```bash
python main.py
```

### Ejecución de las pruebas unitarias
```bash
python -m unittest test_analyzer.py
```

---

## 📊 Resumen de Resultados

### Gramática 1 (Ejercicio 1)
- **PRIMEROS:**
  - $\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$
  - $\text{PRIMEROS}(A) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$
  - $\text{PRIMEROS}(B) = \{\text{cuatro}, \text{seis}, \varepsilon\}$
  - $\text{PRIMEROS}(C) = \{\text{cinco}, \varepsilon\}$
  - $\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$
- **SIGUIENTES:**
  - $\text{SIGUIENTES}(S) = \{\text{dos}, \$\}$
  - $\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$
  - $\text{SIGUIENTES}(B) = \{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$
  - $\text{SIGUIENTES}(C) = \{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$
  - $\text{SIGUIENTES}(D) = \{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$
- **Diagnóstico LL(1):** **NO es LL(1)** (presenta recursión izquierda directa en $S \to S \text{ dos}$ y $A \to A \text{ tres}$, y conflictos en $S, A, B, D$).

### Gramática 2 (Ejercicio 2)
- **PRIMEROS:**
  - $\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$
  - $\text{PRIMEROS}(A) = \{\text{dos}, \varepsilon\}$
  - $\text{PRIMEROS}(B) = \{\text{cinco}, \text{cuatro}, \text{tres}, \varepsilon\}$
  - $\text{PRIMEROS}(C) = \{\text{cinco}, \text{cuatro}\}$
  - $\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$
- **SIGUIENTES:**
  - $\text{SIGUIENTES}(S) = \{\$\}$
  - $\text{SIGUIENTES}(A) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$
  - $\text{SIGUIENTES}(B) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$
  - $\text{SIGUIENTES}(C) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$
  - $\text{SIGUIENTES}(D) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$
- **Diagnóstico LL(1):** **NO es LL(1)** (conflictos de predicción en las reglas alternativas de $B$ y $D$).

---

## 👥 Autor
- **Dylan David Torres** - [@DylanDD17](https://github.com/DylanDD17)
