# Análisis Sintáctico Descendente: Algoritmos LL(1)
### Cálculo y Comparación de Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN

**Asignatura:** Lenguajes de Programación y Transducción  
**Autor:** Dylan David Torres — [GitHub: @DylanDD17](https://github.com/DylanDD17)  
**Entorno de ejecución:** Python 3.8+ (Biblioteca estándar)

---

## 1. Descripción del Proyecto

Este repositorio contiene la solución formal e ingenieril a la tarea del curso:
1. **Deducción analítica:** Cálculo manual y riguroso de los conjuntos de **PRIMEROS**, **SIGUIENTES** y **PREDICCIÓN** para dos gramáticas libres de contexto, siguiendo las definiciones del material de clase.
2. **Implementación computacional en Python:** Algoritmos de punto fijo para PRIMEROS y SIGUIENTES, cálculo de PREDICCIÓN, detección de conflictos y construcción de la tabla predictiva `M[A, a]`.
3. **Comparación directa:** Validación automática y manual al 100% entre la teoría analítica y la ejecución algorítmica, con interpretación de los resultados respecto al criterio LL(1).

---

## 2. Marco Teórico y Fórmulas Matemáticas

Basado en las diapositivas de clase (Unidad de Análisis Sintáctico Descendente):

### 2.1. Símbolos Anulables
Un símbolo no terminal $X$ es **anulable** si deriva en la cadena vacía:
$$X \Rightarrow^* \varepsilon$$

### 2.2. Conjunto PRIMEROS
Contiene los terminales que pueden iniciar una cadena derivada de $\alpha$, incluyendo $\varepsilon$ si $\alpha$ es anulable:
$$\text{PRIMEROS}(\alpha) = \{ a \in \Sigma \mid \alpha \Rightarrow^* a\beta \} \cup \{ \varepsilon \mid \alpha \Rightarrow^* \varepsilon \}$$

Para una secuencia $X_1 X_2 \dots X_k$:
$$\text{PRIMEROS}(X_1 \dots X_k) = \bigcup_{i=1}^{k} (\text{PRIMEROS}(X_i) \setminus \{\varepsilon\}) \quad \text{hasta el primer } X_i \text{ no anulable} \quad [\cup \{\varepsilon\} \text{ si todos son anulables}]$$

### 2.3. Conjunto SIGUIENTES
Contiene los terminales que pueden aparecer inmediatamente a la derecha de $A$ en alguna forma sentencial derivada desde el símbolo inicial $S$:
$$\text{SIGUIENTES}(A) = \{ a \in (\Sigma \cup \{\text{\$}\}) \mid S \Rightarrow^* \mu A a \nu \}$$

**Reglas de propagación (Algoritmo de Punto Fijo):**
1. Inicializar $\text{\$} \in \text{SIGUIENTES}(S)$.
2. Para cada producción $A \to \alpha B \beta$:
   - Agregar $(\text{PRIMEROS}(\beta) \setminus \{\varepsilon\})$ a $\text{SIGUIENTES}(B)$.
   - Si $\beta \Rightarrow^* \varepsilon$ o $\beta$ es vacía, agregar $\text{SIGUIENTES}(A)$ a $\text{SIGUIENTES}(B)$.
3. Repetir hasta que ningún conjunto cambie.
4. **Regla clave:** $\varepsilon$ nunca pertenece a un conjunto SIGUIENTES.

### 2.4. Conjunto de PREDICCIÓN de una Regla
Determina los tokens de anticipación (*lookahead*) válidos para elegir la regla $A \to \alpha$:
$$\text{PRED}(A \to \alpha) = \begin{cases} 
\text{PRIMEROS}(\alpha), & \text{si } \varepsilon \notin \text{PRIMEROS}(\alpha) \\ 
(\text{PRIMEROS}(\alpha) \setminus \{\varepsilon\}) \cup \text{SIGUIENTES}(A), & \text{si } \varepsilon \in \text{PRIMEROS}(\alpha) 
\end{cases}$$

### 2.5. Criterio LL(1)
Una gramática es LL(1) si para todo no terminal $A$, las producciones alternativas tienen predicciones mutuamente disjuntas:
$$\forall (A \to \alpha), (A \to \beta) \text{ con } \alpha \ne \beta : \quad \text{PRED}(A \to \alpha) \cap \text{PRED}(A \to \beta) = \emptyset$$

---

## 3. Deducción Analítica

### 3.1. Gramática 1 (Ejercicio 1)

#### Producciones:
```text
(1) S -> A uno B C        (7)  B -> ε
(2) S -> S dos            (8)  C -> cinco D B
(3) A -> B C D            (9)  C -> ε
(4) A -> A tres           (10) D -> seis
(5) A -> ε                (11) D -> ε
(6) B -> D cuatro C tres
```

#### Análisis paso a paso:
1. **Anulabilidad:** $A, B, C, D$ son anulables ($\varepsilon$). $S$ no es anulable.
2. **PRIMEROS:**
   - $\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$
   - $\text{PRIMEROS}(C) = \{\text{cinco}, \varepsilon\}$
   - $\text{PRIMEROS}(B) = (\text{PRIMEROS}(D) \setminus \{\varepsilon\}) \cup \{\text{cuatro}\} \cup \{\varepsilon\} = \{\text{cuatro}, \text{seis}, \varepsilon\}$
   - $\text{PRIMEROS}(A) = (\text{PRIM}(B)\setminus\{\varepsilon\}) \cup (\text{PRIM}(C)\setminus\{\varepsilon\}) \cup (\text{PRIM}(D)\setminus\{\varepsilon\}) \cup \{\text{tres}\} \cup \{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$
   - $\text{PRIMEROS}(S) = (\text{PRIMEROS}(A) \setminus \{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$
3. **SIGUIENTES:**
   - $S$: Inicial con `$` y de $S \to S \text{ dos}$ recibe `dos` $\implies \text{SIGUIENTES}(S) = \{\text{dos}, \$\}$.
   - $A$: De $S \to A \text{ uno } B C$ recibe `uno`; de $A \to A \text{ tres}$ recibe `tres` $\implies \text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$.
   - $C$: Recibe $\text{SIG}(S)$, $\text{PRIM}(D)\setminus\{\varepsilon\} = \{\text{seis}\}$, $\text{SIG}(A)$, y `tres` $\implies \text{SIGUIENTES}(C) = \{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$.
   - $B$: Recibe $\text{SIG}(C)$ y $\text{PRIM}(C)\setminus\{\varepsilon\} = \{\text{cinco}\}$ $\implies \text{SIGUIENTES}(B) = \{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$.
   - $D$: Recibe `cuatro`, $\text{SIG}(A)$, $\text{PRIM}(B)\setminus\{\varepsilon\}$, y $\text{SIG}(C)$ $\implies \text{SIGUIENTES}(D) = \{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$.

#### Conjuntos de PREDICCIÓN de la Gramática 1:
| Regla | Producción | $\text{PRIMEROS}(\alpha)$ | ¿Anulable? | $\text{PREDICCIÓN}$ |
|:---:|:---|:---|:---:|:---|
| **(1)** | `S -> A uno B C` | `{ cinco, cuatro, seis, tres, uno }` | No | `{ cinco, cuatro, seis, tres, uno }` |
| **(2)** | `S -> S dos` | `{ cinco, cuatro, seis, tres, uno }` | No | `{ cinco, cuatro, seis, tres, uno }` |
| **(3)** | `A -> B C D` | `{ cinco, cuatro, seis, ε }` | **Sí** | `{ cinco, cuatro, seis, tres, uno }` |
| **(4)** | `A -> A tres` | `{ cinco, cuatro, seis, tres }` | No | `{ cinco, cuatro, seis, tres }` |
| **(5)** | `A -> ε` | `{ ε }` | **Sí** | `{ tres, uno }` |
| **(6)** | `B -> D cuatro C tres` | `{ cuatro, seis }` | No | `{ cuatro, seis }` |
| **(7)** | `B -> ε` | `{ ε }` | **Sí** | `{ cinco, dos, seis, tres, uno, $ }` |
| **(8)** | `C -> cinco D B` | `{ cinco }` | No | `{ cinco }` |
| **(9)** | `C -> ε` | `{ ε }` | **Sí** | `{ dos, seis, tres, uno, $ }` |
| **(10)**| `D -> seis` | `{ seis }` | No | `{ seis }` |
| **(11)**| `D -> ε` | `{ ε }` | **Sí** | `{ cuatro, dos, seis, tres, uno, $ }` |

---

### 3.2. Gramática 2 (Ejercicio 2)

#### Producciones:
```text
(1) S -> A B uno       (6)  B -> ε
(2) A -> dos B         (7)  C -> cuatro A B
(3) A -> ε             (8)  C -> cinco
(4) B -> C D           (9)  D -> seis
(5) B -> tres          (10) D -> ε
```

#### Análisis paso a paso:
1. **Anulabilidad:** $A, B, D$ son anulables ($\varepsilon$). $C$ y $S$ no son anulables.
2. **PRIMEROS:**
   - $\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$
   - $\text{PRIMEROS}(C) = \{\text{cuatro}, \text{cinco}\}$
   - $\text{PRIMEROS}(B) = \text{PRIM}(C) \cup \{\text{tres}\} \cup \{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{tres}, \varepsilon\}$
   - $\text{PRIMEROS}(A) = \{\text{dos}, \varepsilon\}$
   - $\text{PRIMEROS}(S) = (\text{PRIM}(A)\setminus\{\varepsilon\}) \cup (\text{PRIM}(B)\setminus\{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$
3. **SIGUIENTES:**
   - $S$: Inicial con `$` y no aparece en la derecha de ninguna regla $\implies \text{SIGUIENTES}(S) = \{\$\}$.
   - De $S \to A B \text{ uno}$: $A$ va seguido de $B \text{ uno}$, recibiendo $\{\text{cinco}, \text{cuatro}, \text{tres}, \text{uno}\}$.
   - Ciclo de inclusión mutua: $\text{SIG}(A) \subseteq \text{SIG}(B) \subseteq \text{SIG}(C) \subseteq \text{SIG}(A)$. Además $D$ aporta `seis` a $C$, el cual se propaga a todos ellos. $D$ recibe $\text{SIG}(B)$.  
     Ninguno contiene `$`, pues siempre están a la izquierda del terminal `uno`.
   - $\text{SIGUIENTES}(A) = \text{SIGUIENTES}(B) = \text{SIGUIENTES}(C) = \text{SIGUIENTES}(D) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$.

#### Conjuntos de PREDICCIÓN de la Gramática 2:
| Regla | Producción | $\text{PRIMEROS}(\alpha)$ | ¿Anulable? | $\text{PREDICCIÓN}$ |
|:---:|:---|:---|:---:|:---|
| **(1)** | `S -> A B uno` | `{ cinco, cuatro, dos, tres, uno }` | No | `{ cinco, cuatro, dos, tres, uno }` |
| **(2)** | `A -> dos B` | `{ dos }` | No | `{ dos }` |
| **(3)** | `A -> ε` | `{ ε }` | **Sí** | `{ cinco, cuatro, seis, tres, uno }` |
| **(4)** | `B -> C D` | `{ cinco, cuatro }` | No | `{ cinco, cuatro }` |
| **(5)** | `B -> tres` | `{ tres }` | No | `{ tres }` |
| **(6)** | `B -> ε` | `{ ε }` | **Sí** | `{ cinco, cuatro, seis, tres, uno }` |
| **(7)** | `C -> cuatro A B` | `{ cuatro }` | No | `{ cuatro }` |
| **(8)** | `C -> cinco` | `{ cinco }` | No | `{ cinco }` |
| **(9)** | `D -> seis` | `{ seis }` | No | `{ seis }` |
| **(10)**| `D -> ε` | `{ ε }` | **Sí** | `{ cinco, cuatro, seis, tres, uno }` |

---

## 4. Implementación en Python

El software se estructuró de forma modular y con pruebas automatizadas:

```text
primeros-siguientes-prediccion/
├── grammar_analyzer.py      # Motor con clases Production y GrammarAnalyzer
├── main.py                  # Ejecución principal con tablas y traza paso a paso
├── test_analyzer.py         # Suite de 8 pruebas unitarias (unittest)
├── INFORME_TEORICO_Y_COMPARATIVO.md  # Informe formal complementario
└── README.md                # Este documento central
```

### Ejecución
```bash
# Ejecutar el programa principal con todas las tablas
python main.py

# Ejecutar las pruebas unitarias automatizadas
python -m unittest test_analyzer.py
```

---

## 5. Comparación Directa de Resultados

### 5.1. ¿Qué se compara?
Se compara el valor exacto de cada conjunto matemático obtenido manualmente mediante deducción teórica contra el conjunto calculado por los algoritmos de punto fijo en Python:
1. Conjuntos **PRIMEROS** de todos los no terminales ($S, A, B, C, D$).
2. Conjuntos **SIGUIENTES** de todos los no terminales ($S, A, B, C, D$).
3. Conjuntos de **PREDICCIÓN** de cada una de las producciones individuales (11 reglas en Gramática 1; 10 reglas en Gramática 2).

### 5.2. Tablas de Comparación

#### Gramática 1
| Conjunto / Regla | Valor Analítico | Valor Computacional | Coincidencia |
|:---|:---|:---|:---:|
| $\text{PRIMEROS}(S)$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(A)$ | `{ cinco, cuatro, seis, tres, ε }` | `{ cinco, cuatro, seis, tres, ε }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(B)$ | `{ cuatro, seis, ε }` | `{ cuatro, seis, ε }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(C)$ | `{ cinco, ε }` | `{ cinco, ε }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(D)$ | `{ seis, ε }` | `{ seis, ε }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(S)$ | `{ dos, $ }` | `{ dos, $ }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(A)$ | `{ tres, uno }` | `{ tres, uno }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(B)$ | `{ cinco, dos, seis, tres, uno, $ }` | `{ cinco, dos, seis, tres, uno, $ }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(C)$ | `{ dos, seis, tres, uno, $ }` | `{ dos, seis, tres, uno, $ }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(D)$ | `{ cuatro, dos, seis, tres, uno, $ }` | `{ cuatro, dos, seis, tres, uno, $ }` | **✓ 100% Exacto** |
| $\text{PRED}(\text{Reglas } 1 \dots 11)$ | Coincidencia idéntica regla por regla | Coincidencia idéntica regla por regla | **✓ 100% Exacto** |

#### Gramática 2
| Conjunto / Regla | Valor Analítico | Valor Computacional | Coincidencia |
|:---|:---|:---|:---:|
| $\text{PRIMEROS}(S)$ | `{ cinco, cuatro, dos, tres, uno }` | `{ cinco, cuatro, dos, tres, uno }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(A)$ | `{ dos, ε }` | `{ dos, ε }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(B)$ | `{ cinco, cuatro, tres, ε }` | `{ cinco, cuatro, tres, ε }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(C)$ | `{ cinco, cuatro }` | `{ cinco, cuatro }` | **✓ 100% Exacto** |
| $\text{PRIMEROS}(D)$ | `{ seis, ε }` | `{ seis, ε }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(S)$ | `{ $ }` | `{ $ }` | **✓ 100% Exacto** |
| $\text{SIGUIENTES}(A, B, C, D)$ | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **✓ 100% Exacto** |
| $\text{PRED}(\text{Reglas } 1 \dots 10)$ | Coincidencia idéntica regla por regla | Coincidencia idéntica regla por regla | **✓ 100% Exacto** |

---

## 6. ¿Qué significan estos resultados?

### 6.1. Validación Matemática del Software
La correspondencia del 100% demuestra que:
* La lógica de propagación con anulabilidad en secuencias arbitrarias fue implementada correctamente sin ignorar casos en los que símbolos intermedios se anulan.
* El algoritmo de punto fijo alcanza la convergencia en un número finito de pasos (garantizado teóricamente por la finitud del vocabulario).

### 6.2. Diagnóstico del Criterio LL(1)

#### Gramática 1: NO es LL(1)
1. **Recursión por la izquierda directa:** Presenta $S \to S \text{ dos}$ y $A \to A \text{ tres}$. En un analizador descendente recursivo, esto genera recursión infinita inmediata antes de consumir tokens.
2. **Colisiones masivas de predicción:** Las alternativas de $S$, $A$, $B$ y $D$ se solapan ampliamente. Por ejemplo, al expandir $S$ con el token `uno`, el analizador no sabe si aplicar la regla (1) o la regla (2).

#### Gramática 2: NO es LL(1)
1. Aunque carece de recursión izquierda y las reglas de $A$ y $C$ son mutuamente disjuntas:
   - $\text{PRED}(A \to \text{dos } B) \cap \text{PRED}(A \to \varepsilon) = \{\text{dos}\} \cap \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\} = \emptyset$ (Sin conflicto).
   - $\text{PRED}(C \to \text{cuatro } A B) \cap \text{PRED}(C \to \text{cinco}) = \{\text{cuatro}\} \cap \{\text{cinco}\} = \emptyset$ (Sin conflicto).
2. **Conflictos en $B$ y $D$:**
   - Para $B$: la regla vacía $B \to \varepsilon$ colisiona con $B \to C D$ en los tokens `cuatro` y `cinco`, y con $B \to \text{tres}$ en `tres`.
   - Para $D$: $D \to \text{seis}$ y $D \to \varepsilon$ colisionan en el token `seis`.

### 6.3. Conclusión Práctica para el Compilador
En ambas gramáticas, un analizador LL(1) **no puede operar de manera determinista** con una anticipación de 1 token (*lookahead* = 1), dado que las tablas de análisis contienen celdas con más de una producción. Para poder analizarlas de forma predictiva descendente, requerirían transformaciones de gramática (eliminación de recursión izquierda y factorización).
