# Algoritmos de Primeros, Siguientes y Predicción

**Asignatura:** Lenguajes de Programación y Transducción  
**Autor:** Dylan David Torres — [GitHub: @DylanDD17](https://github.com/DylanDD17)  
**Entorno:** Python 3.8+ (Biblioteca estándar)

---

## 1. ¿En qué consiste?

Este proyecto implementa en Python los algoritmos fundamentales del análisis sintáctico descendente para Gramáticas Libres de Contexto (GLC):
1. **Algoritmo de PRIMEROS:** Determina el conjunto de terminales que pueden aparecer al inicio de una cadena derivada por una forma sentencial o símbolo no terminal. Si la secuencia puede anularse completamente, se incluye la cadena vacía $\varepsilon$.
2. **Algoritmo de SIGUIENTES:** Determina el conjunto de terminales (incluyendo el marcador de fin de entrada `$`) que pueden aparecer inmediatamente a la derecha de un no terminal en alguna forma sentencial válida derivable desde el símbolo inicial.
3. **Algoritmo de PREDICCIÓN:** Determina el conjunto de símbolos directores (*lookahead*) que permiten seleccionar de forma unívoca y determinista qué regla de producción aplicar al expandir un no terminal.

El sistema carga gramáticas desde archivos de texto plano (`.txt`), ejecuta los algoritmos mediante iteraciones de punto fijo hasta alcanzar la convergencia, genera tablas formateadas en consola y valida la equivalencia exacta con las deducciones analíticas de clase.

---

## 2. Archivos del Repositorio

* **`analizador.py`**: Programa principal en Python. Implementa la lectura de gramáticas `.txt`, la construcción de los conjuntos mediante punto fijo y la impresión de tablas.
* **`ejercicio1.txt`**: Archivo de texto con las producciones de la gramática del Ejercicio 1.
* **`ejercicio2.txt`**: Archivo de texto con las producciones de la gramática del Ejercicio 2.
* **`capturas/`**: Directorio con evidencias gráficas de la ejecución en consola.
  * `salida_ejercicio1.png`: Captura de terminal del Ejercicio 1.
  * `salida_ejercicio2.png`: Captura de terminal del Ejercicio 2.
* **`README.md`**: Informe técnico y documentación completa del proyecto.
* **`.gitignore`**: Configuración de exclusiones de Git.

---

## 3. Estructura del Proyecto

```text
primeros-siguientes-prediccion/
├── capturas/
│   ├── salida_ejercicio1.png
│   └── salida_ejercicio2.png
├── analizador.py
├── ejercicio1.txt
├── ejercicio2.txt
├── .gitignore
└── README.md
```

---

## 4. Requisitos

* **Python 3.8** o superior instalado.
* No requiere librerías externas ni gestores de paquetes adicionales (diseñado exclusivamente con la biblioteca estándar de Python).

---

## 5. Cómo Ejecutarlo

Desde la terminal en la raíz del repositorio:

### Ejecutar ambos ejercicios automáticamente:
```bash
python analizador.py
```

### Ejecutar un archivo específico:
```bash
python analizador.py ejercicio1.txt
```
```bash
python analizador.py ejercicio2.txt
```

---

## 6. Resultados Analíticos

### 6.1. Ejercicio 1

#### Gramática:
```text
S -> A uno B C
S -> S dos
A -> B C D
A -> A tres
A -> ε
B -> D cuatro C tres
B -> ε
C -> cinco D B
C -> ε
D -> seis
D -> ε
```

* **No Terminales:** `S`, `A`, `B`, `C`, `D`  
* **Terminales:** `cinco`, `cuatro`, `dos`, `seis`, `tres`, `uno`  
* **Símbolo Inicial:** `S`

#### Análisis y Deducción Paso a Paso:
1. **Deducción de PRIMEROS:**
   * Para **$D$**: Las reglas $D \to \text{seis}$ y $D \to \varepsilon$ generan directamente $\{\text{seis}, \varepsilon\}$.
   * Para **$C$**: $C \to \text{cinco } D B$ aporta `cinco` y $C \to \varepsilon$ aporta $\varepsilon$. Así, $\text{PRIMEROS}(C) = \{\text{cinco}, \varepsilon\}$.
   * Para **$B$**: En $B \to D \text{ cuatro } C \text{ tres}$, como $\varepsilon \in \text{PRIMEROS}(D)$, la secuencia toma $(\text{PRIMEROS}(D) \setminus \{\varepsilon\}) \cup \{\text{cuatro}\} = \{\text{cuatro}, \text{seis}\}$. Con $B \to \varepsilon$, resulta $\{\text{cuatro}, \text{seis}, \varepsilon\}$.
   * Para **$A$**: En $A \to B C D$, dado que $B$, $C$ y $D$ pueden anularse, se acumulan sucesivamente los terminales de los tres: $(\text{PRIM}(B)\setminus\{\varepsilon\}) \cup (\text{PRIM}(C)\setminus\{\varepsilon\}) \cup (\text{PRIM}(D)\setminus\{\varepsilon\}) \cup \{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \varepsilon\}$. Además, en $A \to A \text{ tres}$, como $A \Rightarrow^* \varepsilon$, se puede derivar $A \Rightarrow A \text{ tres} \Rightarrow \varepsilon \text{ tres} = \text{tres}$, incorporando `tres`. Por tanto, $\text{PRIMEROS}(A) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$.
   * Para **$S$**: En $S \to A \text{ uno } B C$, como $A$ es anulable, toma $(\text{PRIMEROS}(A)\setminus\{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$. La regla $S \to S \text{ dos}$ no añade símbolos nuevos.

2. **Deducción de SIGUIENTES:**
   * Por definición, el marcador de fin de entrada `$` se inicializa en el símbolo inicial: $\text{SIGUIENTES}(S) = \{\$\}$.
   * En $S \to S \text{ dos}$, $S$ es seguido directamente por `dos`, por lo que $\text{SIGUIENTES}(S) = \{\text{dos}, \$\}$.
   * En $S \to A \text{ uno } B C$, $A$ va seguido de `uno` $\implies \text{uno} \in \text{SIGUIENTES}(A)$. Por $A \to A \text{ tres}$, $A$ es seguido de `tres` $\implies \text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
   * En $S \to A \text{ uno } B C$, $B$ es seguido por $C$, recibiendo $(\text{PRIMEROS}(C)\setminus\{\varepsilon\}) = \{\text{cinco}\}$; como $C \Rightarrow^* \varepsilon$, también recibe $\text{SIGUIENTES}(S) = \{\text{dos}, \$\}$. Además, $C$ queda al final, por lo que recibe $\text{SIGUIENTES}(S)$.
   * En $A \to B C D$, $B$ es seguido por $C D$, recibiendo $\{\text{cinco}, \text{seis}\}$ y $\text{SIGUIENTES}(A)$. $C$ es seguido por $D$, recibiendo `seis` y $\text{SIGUIENTES}(A)$. $D$ queda al final, recibiendo $\text{SIGUIENTES}(A)$.
   * En $B \to D \text{ cuatro } C \text{ tres}$, $D$ recibe `cuatro` y $C$ recibe `tres`.
   * En $C \to \text{cinco } D B$, $D$ recibe $(\text{PRIMEROS}(B)\setminus\{\varepsilon\}) = \{\text{cuatro}, \text{seis}\}$ y $\text{SIGUIENTES}(C)$. A su vez, $B$ queda al final, recibiendo $\text{SIGUIENTES}(C)$.
   * Al alcanzar el punto fijo de propagación transitiva, se obtienen los conjuntos mostrados en la tabla.

3. **Deducción de PREDICCIÓN:**
   * Para producciones no anulables (reglas 1, 2, 4, 6, 8 y 10), el conjunto director corresponde directamente a $\text{PRIMEROS}(\alpha)$.
   * Para producciones anulables (reglas 3, 5, 7, 9 y 11), el conjunto director incorpora la unión con $\text{SIGUIENTES}$ del no terminal del lado izquierdo: $(\text{PRIMEROS}(\alpha) \setminus \{\varepsilon\}) \cup \text{SIGUIENTES}(A)$.

#### Tabla de PRIMEROS:
| No Terminal | PRIMEROS |
|:---:|:---|
| **S** | `{ cinco, cuatro, seis, tres, uno }` |
| **A** | `{ cinco, cuatro, seis, tres, ε }` |
| **B** | `{ cuatro, seis, ε }` |
| **C** | `{ cinco, ε }` |
| **D** | `{ seis, ε }` |

#### Tabla de SIGUIENTES:
| No Terminal | SIGUIENTES |
|:---:|:---|
| **S** | `{ dos, $ }` |
| **A** | `{ tres, uno }` |
| **B** | `{ cinco, dos, seis, tres, uno, $ }` |
| **C** | `{ dos, seis, tres, uno, $ }` |
| **D** | `{ cuatro, dos, seis, tres, uno, $ }` |

#### Tabla de PREDICCIÓN:
| Regla | Producción | PREDICCIÓN |
|:---:|:---|:---|
| **(1)** | `S -> A uno B C` | `{ cinco, cuatro, seis, tres, uno }` |
| **(2)** | `S -> S dos` | `{ cinco, cuatro, seis, tres, uno }` |
| **(3)** | `A -> B C D` | `{ cinco, cuatro, seis, tres, uno }` |
| **(4)** | `A -> A tres` | `{ cinco, cuatro, seis, tres }` |
| **(5)** | `A -> ε` | `{ tres, uno }` |
| **(6)** | `B -> D cuatro C tres` | `{ cuatro, seis }` |
| **(7)** | `B -> ε` | `{ cinco, dos, seis, tres, uno, $ }` |
| **(8)** | `C -> cinco D B` | `{ cinco }` |
| **(9)** | `C -> ε` | `{ dos, seis, tres, uno, $ }` |
| **(10)** | `D -> seis` | `{ seis }` |
| **(11)** | `D -> ε` | `{ cuatro, dos, seis, tres, uno, $ }` |

#### Diagnóstico LL(1) de la Gramática 1:
La gramática **NO es LL(1)** por dos motivos críticos:
* **Recursión por la izquierda directa:** Las reglas $S \to S \text{ dos}$ y $A \to A \text{ tres}$ causan que un analizador sintáctico descendente recursivo entre en bucle infinito sin llegar a consumir tokens de entrada.
* **Colisión de conjuntos de predicción:** Para $S$, las reglas (1) y (2) comparten exactamente el mismo conjunto director (`cinco`, `cuatro`, `seis`, `tres`, `uno`). Similarmente, en $A$, $B$ y $D$ las reglas alternativas comparten tokens de anticipación, haciendo imposible la decisión determinista con *lookahead* = 1.

---

### 6.2. Ejercicio 2

#### Gramática:
```text
S -> A B uno
A -> dos B
A -> ε
B -> C D
B -> tres
B -> ε
C -> cuatro A B
C -> cinco
D -> seis
D -> ε
```

* **No Terminales:** `S`, `A`, `B`, `C`, `D`  
* **Terminales:** `cinco`, `cuatro`, `dos`, `seis`, `tres`, `uno`  
* **Símbolo Inicial:** `S`

#### Análisis y Deducción Paso a Paso:
1. **Deducción de PRIMEROS:**
   * Para **$D$**: Las reglas $D \to \text{seis}$ y $D \to \varepsilon$ dan $\{\text{seis}, \varepsilon\}$.
   * Para **$C$**: Ambas reglas inician con terminales: $C \to \text{cuatro } A B$ aporta `cuatro` y $C \to \text{cinco}$ aporta `cinco`. Como ninguna deriva en $\varepsilon$, $\text{PRIMEROS}(C) = \{\text{cuatro}, \text{cinco}\}$.
   * Para **$B$**: En $B \to C D$, como $\varepsilon \notin \text{PRIMEROS}(C)$, la derivación se detiene en $C$, tomando únicamente $\text{PRIMEROS}(C) = \{\text{cuatro}, \text{cinco}\}$. Sumando $B \to \text{tres}$ y $B \to \varepsilon$, se obtiene $\{\text{cinco}, \text{cuatro}, \text{tres}, \varepsilon\}$.
   * Para **$A$**: $A \to \text{dos } B$ aporta `dos` y $A \to \varepsilon$ aporta $\varepsilon$. Así, $\text{PRIMEROS}(A) = \{\text{dos}, \varepsilon\}$.
   * Para **$S$**: En $S \to A B \text{ uno}$, al ser $A$ anulable se toma $(\text{PRIMEROS}(A)\setminus\{\varepsilon\}) = \{\text{dos}\}$. Al ser $B$ también anulable, se continúa y se toma $(\text{PRIMEROS}(B)\setminus\{\varepsilon\}) = \{\text{cinco}, \text{cuatro}, \text{tres}\}$. Finalmente, como ambos se anulan, se llega al terminal `uno`. Así, $\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$.

2. **Deducción de SIGUIENTES:**
   * Inicialización: $\text{SIGUIENTES}(S) = \{\$\}$. Dado que $S$ no aparece en el lado derecho de ninguna producción, el marcador de fin de entrada `$` no se propaga a ningún otro símbolo.
   * En $S \to A B \text{ uno}$: $A$ es seguido por $B \text{ uno}$, recibiendo $(\text{PRIMEROS}(B)\setminus\{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{tres}, \text{uno}\}$. Por su parte, $B$ es seguido de `uno` $\implies \text{uno} \in \text{SIGUIENTES}(B)$.
   * Se forma un ciclo de dependencia mutua entre no terminales:
     * $A \to \text{dos } B \implies \text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(B)$.
     * $B \to C D \implies C$ recibe `seis` de $D$, y como $D \Rightarrow^* \varepsilon$, recibe también $\text{SIGUIENTES}(B)$. Además, $D$ queda al final, por lo que recibe $\text{SIGUIENTES}(B)$.
     * $C \to \text{cuatro } A B \implies A$ recibe $(\text{PRIMEROS}(B)\setminus\{\varepsilon\})$ y $\text{SIGUIENTES}(C)$. A su vez, $B$ queda al final y recibe $\text{SIGUIENTES}(C)$.
   * Al propagarse en el ciclo transitivo $\text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(B) \subseteq \text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(A)$, los tres conjuntos incorporan todos los símbolos y el terminal `seis`. Finalmente, $D$ recibe $\text{SIGUIENTES}(B)$.
   * En consecuencia, $A, B, C, D$ convergen exactamente al mismo conjunto: $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$. Ninguno contiene `$`, ya que en cualquier forma sentencial siempre están seguidos al menos por el terminal `uno`.

3. **Deducción de PREDICCIÓN:**
   * Las reglas (1), (2), (4), (5), (7), (8) y (9) no son anulables, por lo que su conjunto director equivale a $\text{PRIMEROS}(\alpha)$.
   * Las reglas (3) $A \to \varepsilon$, (6) $B \to \varepsilon$ y (10) $D \to \varepsilon$ toman sus respectivos conjuntos $\text{SIGUIENTES}$.

#### Tabla de PRIMEROS:
| No Terminal | PRIMEROS |
|:---:|:---|
| **S** | `{ cinco, cuatro, dos, tres, uno }` |
| **A** | `{ dos, ε }` |
| **B** | `{ cinco, cuatro, tres, ε }` |
| **C** | `{ cinco, cuatro }` |
| **D** | `{ seis, ε }` |

#### Tabla de SIGUIENTES:
| No Terminal | SIGUIENTES |
|:---:|:---|
| **S** | `{ $ }` |
| **A** | `{ cinco, cuatro, seis, tres, uno }` |
| **B** | `{ cinco, cuatro, seis, tres, uno }` |
| **C** | `{ cinco, cuatro, seis, tres, uno }` |
| **D** | `{ cinco, cuatro, seis, tres, uno }` |

#### Tabla de PREDICCIÓN:
| Regla | Producción | PREDICCIÓN |
|:---:|:---|:---|
| **(1)** | `S -> A B uno` | `{ cinco, cuatro, dos, tres, uno }` |
| **(2)** | `A -> dos B` | `{ dos }` |
| **(3)** | `A -> ε` | `{ cinco, cuatro, seis, tres, uno }` |
| **(4)** | `B -> C D` | `{ cinco, cuatro }` |
| **(5)** | `B -> tres` | `{ tres }` |
| **(6)** | `B -> ε` | `{ cinco, cuatro, seis, tres, uno }` |
| **(7)** | `C -> cuatro A B` | `{ cuatro }` |
| **(8)** | `C -> cinco` | `{ cinco }` |
| **(9)** | `D -> seis` | `{ seis }` |
| **(10)** | `D -> ε` | `{ cinco, cuatro, seis, tres, uno }` |

#### Diagnóstico LL(1) de la Gramática 2:
La gramática **NO es LL(1)**:
* A diferencia del Ejercicio 1, esta gramática **no posee recursión izquierda** y las reglas alternativas de $A$ y de $C$ son mutuamente disjuntas:
  * $\text{PRED}(A \to \text{dos } B) \cap \text{PRED}(A \to \varepsilon) = \{\text{dos}\} \cap \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\} = \emptyset$.
  * $\text{PRED}(C \to \text{cuatro } A B) \cap \text{PRED}(C \to \text{cinco}) = \{\text{cuatro}\} \cap \{\text{cinco}\} = \emptyset$.
* Sin embargo, presenta colisiones en los no terminales $B$ y $D$:
  * Para $B$: La regla vacía (6) $B \to \varepsilon$ colisiona con la regla (4) en `cuatro` y `cinco`, y con la regla (5) en `tres`.
  * Para $D$: La regla (9) $D \to \text{seis}$ y la regla (10) $D \to \varepsilon$ colisionan en el símbolo `seis`.
* Por lo tanto, al construir la tabla de análisis sintáctico $M$, las celdas $M[B, \text{tres}]$, $M[B, \text{cuatro}]$, $M[B, \text{cinco}]$ y $M[D, \text{seis}]$ contienen más de una regla de producción, impidiendo un análisis determinista con 1 token de anticipación.

---

## 7. Comparación de Resultados

Se contrastaron elemento por elemento los conjuntos derivados de forma analítica manual con los calculados automáticamente por el analizador en Python (`analizador.py`).

### 7.1. Tabla de Comparación - Ejercicio 1

| Elemento | Resultado Analítico | Resultado Computacional | Diagnóstico |
|:---|:---|:---|:---:|
| `PRIMEROS(S)` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | Coincide |
| `PRIMEROS(A)` | `{ cinco, cuatro, seis, tres, ε }` | `{ cinco, cuatro, seis, tres, ε }` | Coincide |
| `PRIMEROS(B)` | `{ cuatro, seis, ε }` | `{ cuatro, seis, ε }` | Coincide |
| `PRIMEROS(C)` | `{ cinco, ε }` | `{ cinco, ε }` | Coincide |
| `PRIMEROS(D)` | `{ seis, ε }` | `{ seis, ε }` | Coincide |
| `SIGUIENTES(S)` | `{ dos, $ }` | `{ dos, $ }` | Coincide |
| `SIGUIENTES(A)` | `{ tres, uno }` | `{ tres, uno }` | Coincide |
| `SIGUIENTES(B)` | `{ cinco, dos, seis, tres, uno, $ }` | `{ cinco, dos, seis, tres, uno, $ }` | Coincide |
| `SIGUIENTES(C)` | `{ dos, seis, tres, uno, $ }` | `{ dos, seis, tres, uno, $ }` | Coincide |
| `SIGUIENTES(D)` | `{ cuatro, dos, seis, tres, uno, $ }` | `{ cuatro, dos, seis, tres, uno, $ }` | Coincide |
| `PRED(Reglas 1-11)` | Idénticos regla por regla | Idénticos regla por regla | Coincide |

### 7.2. Tabla de Comparación - Ejercicio 2

| Elemento | Resultado Analítico | Resultado Computacional | Diagnóstico |
|:---|:---|:---|:---:|
| `PRIMEROS(S)` | `{ cinco, cuatro, dos, tres, uno }` | `{ cinco, cuatro, dos, tres, uno }` | Coincide |
| `PRIMEROS(A)` | `{ dos, ε }` | `{ dos, ε }` | Coincide |
| `PRIMEROS(B)` | `{ cinco, cuatro, tres, ε }` | `{ cinco, cuatro, tres, ε }` | Coincide |
| `PRIMEROS(C)` | `{ cinco, cuatro }` | `{ cinco, cuatro }` | Coincide |
| `PRIMEROS(D)` | `{ seis, ε }` | `{ seis, ε }` | Coincide |
| `SIGUIENTES(S)` | `{ $ }` | `{ $ }` | Coincide |
| `SIGUIENTES(A..D)` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | Coincide |
| `PRED(Reglas 1-10)` | Idénticos regla por regla | Idénticos regla por regla | Coincide |

---

## 8. Capturas de Salida del Programa

A continuación se presentan las capturas de ejecución del programa `analizador.py` para cada una de las gramáticas:

### Salida para Ejercicio 1 (`python analizador.py ejercicio1.txt`):
![Salida Ejercicio 1](capturas/salida_ejercicio1.png)

---

### Salida para Ejercicio 2 (`python analizador.py ejercicio2.txt`):
![Salida Ejercicio 2](capturas/salida_ejercicio2.png)

---

## 9. Conclusiones

1. **Correspondencia Teórico-Computacional Plena:**  
   La validación comparativa demostró una coincidencia del 100% entre las derivaciones analíticas manuales y la salida del programa en Python. Esto confirma que el algoritmo de punto fijo modela con precisión la propagación transitiva y resuelve correctamente secuencias con múltiples símbolos anulables consecutivos.

2. **Criterio de Determinismo LL(1):**  
   El cálculo de los conjuntos de predicción evidencia que la condición necesaria y suficiente para que una gramática sea analizable de forma determinista descendente con un token de anticipación es que todas las reglas alternativas de cada no terminal posean conjuntos directores disjuntos. Cuando esta propiedad no se cumple, el analizador experimenta ambigüedad local en la selección de producciones.

3. **Diagnóstico Práctico de las Gramáticas Evaluadas:**  
   * La **Gramática 1** es completamente inviable para análisis LL(1) directo debido a la presencia de recursión por la izquierda (en $S$ y $A$) y colisiones múltiples en sus predicciones.
   * La **Gramática 2**, a pesar de estar libre de recursión izquierda y contar con alternativas disjuntas en $A$ y $C$, fracasa en cumplir el criterio LL(1) debido a los solapamientos originados por las producciones anulables de $B$ y $D$.
   * En un compilador real, ambas gramáticas requerirían una fase previa de transformación sintáctica (eliminación sistemática de recursión izquierda y factorización por la izquierda) para poder ser procesadas por un motor de análisis predictivo.
