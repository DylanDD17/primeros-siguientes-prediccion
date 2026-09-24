# Informe Técnico: Análisis Sintáctico Descendente LL(1)
### Algoritmos y Validación de Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN

**Curso:** Lenguajes de Programación y Transducción  
**Autor:** Dylan David Torres — [GitHub: @DylanDD17](https://github.com/DylanDD17)  
**Fecha:** Septiembre 2026  

---

## 1. Fundamentos Teóricos

El análisis sintáctico descendente construye derivaciones por la izquierda partiendo del símbolo inicial hacia la cadena de entrada. Para lograr tiempo lineal $\mathcal{O}(n)$ con un token de anticipación (*lookahead*), se emplean los siguientes conjuntos (según las diapositivas de clase):

1. **PRIMEROS($\alpha$):**
   $$\text{PRIMEROS}(\alpha) = \{ a \in \Sigma \mid \alpha \Rightarrow^* a\beta \} \cup \{ \varepsilon \mid \alpha \Rightarrow^* \varepsilon \}$$
   Para una secuencia $X_1 X_2 \dots X_k$:
   $$\text{PRIMEROS}(X_1 \dots X_k) = \bigcup_{i=1}^k (\text{PRIMEROS}(X_i) \setminus \{\varepsilon\}) \quad \text{hasta el primer } X_i \text{ no anulable} \quad [\cup \{\varepsilon\} \text{ si todos son anulables}]$$

2. **SIGUIENTES($A$):**
   $$\text{SIGUIENTES}(A) = \{ a \in (\Sigma \cup \{\text{\$}\}) \mid S \Rightarrow^* \mu A a \nu \}$$
   - Inicializar $\text{\$} \in \text{SIGUIENTES}(S)$.
   - Para toda producción $A \to \alpha B \beta$: agregar $(\text{PRIMEROS}(\beta) \setminus \{\varepsilon\})$ a $\text{SIGUIENTES}(B)$.
   - Si $\beta \Rightarrow^* \varepsilon$ o $\beta$ es vacía: agregar $\text{SIGUIENTES}(A)$ a $\text{SIGUIENTES}(B)$.
   - **Regla:** $\varepsilon$ nunca pertenece a un conjunto SIGUIENTES.

3. **PREDICCIÓN($A \to \alpha$):**
   $$\text{PRED}(A \to \alpha) = \begin{cases} 
   \text{PRIMEROS}(\alpha), & \text{si } \varepsilon \notin \text{PRIMEROS}(\alpha) \\ 
   (\text{PRIMEROS}(\alpha) \setminus \{\varepsilon\}) \cup \text{SIGUIENTES}(A), & \text{si } \varepsilon \in \text{PRIMEROS}(\alpha) 
   \end{cases}$$

4. **Criterio LL(1):**
   Para cada no terminal $A$, todas sus producciones alternativas deben tener conjuntos de predicción mutuamente disjuntos:
   $$\text{PRED}(A \to \alpha) \cap \text{PRED}(A \to \beta) = \emptyset \quad (\alpha \ne \beta)$$

---

## 2. Resultados Analíticos

### 2.1. Gramática 1 (Ejercicio 1)

* **No terminales:** $S, A, B, C, D$ (Símbolo inicial: $S$)
* **Terminales:** `uno`, `dos`, `tres`, `cuatro`, `cinco`, `seis`
* **Anulabilidad:** $A, B, C, D$ son anulables ($\Rightarrow^* \varepsilon$). $S$ **no** es anulable.

#### Conjuntos PRIMEROS y SIGUIENTES:
| No Terminal | PRIMEROS | SIGUIENTES |
|:---:|:---|:---|
| **S** | `{ cinco, cuatro, seis, tres, uno }` | `{ dos, $ }` |
| **A** | `{ cinco, cuatro, seis, tres, ε }` | `{ tres, uno }` |
| **B** | `{ cuatro, seis, ε }` | `{ cinco, dos, seis, tres, uno, $ }` |
| **C** | `{ cinco, ε }` | `{ dos, seis, tres, uno, $ }` |
| **D** | `{ seis, ε }` | `{ cuatro, dos, seis, tres, uno, $ }` |

#### Conjuntos de PREDICCIÓN:
* `(1) S -> A uno B C` $\implies$ `{ cinco, cuatro, seis, tres, uno }`
* `(2) S -> S dos` $\implies$ `{ cinco, cuatro, seis, tres, uno }`
* `(3) A -> B C D` $\implies$ `{ cinco, cuatro, seis, tres, uno }`
* `(4) A -> A tres` $\implies$ `{ cinco, cuatro, seis, tres }`
* `(5) A -> ε` $\implies$ `{ tres, uno }`
* `(6) B -> D cuatro C tres` $\implies$ `{ cuatro, seis }`
* `(7) B -> ε` $\implies$ `{ cinco, dos, seis, tres, uno, $ }`
* `(8) C -> cinco D B` $\implies$ `{ cinco }`
* `(9) C -> ε` $\implies$ `{ dos, seis, tres, uno, $ }`
* `(10) D -> seis` $\implies$ `{ seis }`
* `(11) D -> ε` $\implies$ `{ cuatro, dos, seis, tres, uno, $ }`

---

### 2.2. Gramática 2 (Ejercicio 2)

* **No terminales:** $S, A, B, C, D$ (Símbolo inicial: $S$)
* **Terminales:** `uno`, `dos`, `tres`, `cuatro`, `cinco`, `seis`
* **Anulabilidad:** $A, B, D$ son anulables ($\Rightarrow^* \varepsilon$). $S$ y $C$ **no** son anulables.

#### Conjuntos PRIMEROS y SIGUIENTES:
| No Terminal | PRIMEROS | SIGUIENTES |
|:---:|:---|:---|
| **S** | `{ cinco, cuatro, dos, tres, uno }` | `{ $ }` |
| **A** | `{ dos, ε }` | `{ cinco, cuatro, seis, tres, uno }` |
| **B** | `{ cinco, cuatro, tres, ε }` | `{ cinco, cuatro, seis, tres, uno }` |
| **C** | `{ cinco, cuatro }` | `{ cinco, cuatro, seis, tres, uno }` |
| **D** | `{ seis, ε }` | `{ cinco, cuatro, seis, tres, uno }` |

#### Conjuntos de PREDICCIÓN:
* `(1) S -> A B uno` $\implies$ `{ cinco, cuatro, dos, tres, uno }`
* `(2) A -> dos B` $\implies$ `{ dos }`
* `(3) A -> ε` $\implies$ `{ cinco, cuatro, seis, tres, uno }`
* `(4) B -> C D` $\implies$ `{ cinco, cuatro }`
* `(5) B -> tres` $\implies$ `{ tres }`
* `(6) B -> ε` $\implies$ `{ cinco, cuatro, seis, tres, uno }`
* `(7) C -> cuatro A B` $\implies$ `{ cuatro }`
* `(8) C -> cinco` $\implies$ `{ cinco }`
* `(9) D -> seis` $\implies$ `{ seis }`
* `(10) D -> ε` $\implies$ `{ cinco, cuatro, seis, tres, uno }`

---

## 3. Comparación Directa de Resultados

### 3.1. ¿Qué se compara?
Se compara cada conjunto teórico deducido manualmente contra la salida computacional generada por el algoritmo de punto fijo en Python (`grammar_analyzer.py`):
1. Los conjuntos **PRIMEROS** de los 5 no terminales.
2. Los conjuntos **SIGUIENTES** de los 5 no terminales.
3. Los conjuntos de **PREDICCIÓN** de cada producción (21 reglas en total).

### 3.2. Tabla de Comparación - Gramática 1
| Elemento | Resultado Analítico | Resultado Computacional | Diagnóstico |
|:---|:---|:---|:---:|
| `PRIMEROS(S)` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **✓ Coincide (100%)** |
| `PRIMEROS(A)` | `{ cinco, cuatro, seis, tres, ε }` | `{ cinco, cuatro, seis, tres, ε }` | **✓ Coincide (100%)** |
| `PRIMEROS(B)` | `{ cuatro, seis, ε }` | `{ cuatro, seis, ε }` | **✓ Coincide (100%)** |
| `PRIMEROS(C)` | `{ cinco, ε }` | `{ cinco, ε }` | **✓ Coincide (100%)** |
| `PRIMEROS(D)` | `{ seis, ε }` | `{ seis, ε }` | **✓ Coincide (100%)** |
| `SIGUIENTES(S)` | `{ dos, $ }` | `{ dos, $ }` | **✓ Coincide (100%)** |
| `SIGUIENTES(A)` | `{ tres, uno }` | `{ tres, uno }` | **✓ Coincide (100%)** |
| `SIGUIENTES(B)` | `{ cinco, dos, seis, tres, uno, $ }` | `{ cinco, dos, seis, tres, uno, $ }` | **✓ Coincide (100%)** |
| `SIGUIENTES(C)` | `{ dos, seis, tres, uno, $ }` | `{ dos, seis, tres, uno, $ }` | **✓ Coincide (100%)** |
| `SIGUIENTES(D)` | `{ cuatro, dos, seis, tres, uno, $ }` | `{ cuatro, dos, seis, tres, uno, $ }` | **✓ Coincide (100%)** |
| `PRED(Reglas 1-11)` | Idénticos regla por regla | Idénticos regla por regla | **✓ Coincide (100%)** |

### 3.3. Tabla de Comparación - Gramática 2
| Elemento | Resultado Analítico | Resultado Computacional | Diagnóstico |
|:---|:---|:---|:---:|
| `PRIMEROS(S)` | `{ cinco, cuatro, dos, tres, uno }` | `{ cinco, cuatro, dos, tres, uno }` | **✓ Coincide (100%)** |
| `PRIMEROS(A)` | `{ dos, ε }` | `{ dos, ε }` | **✓ Coincide (100%)** |
| `PRIMEROS(B)` | `{ cinco, cuatro, tres, ε }` | `{ cinco, cuatro, tres, ε }` | **✓ Coincide (100%)** |
| `PRIMEROS(C)` | `{ cinco, cuatro }` | `{ cinco, cuatro }` | **✓ Coincide (100%)** |
| `PRIMEROS(D)` | `{ seis, ε }` | `{ seis, ε }` | **✓ Coincide (100%)** |
| `SIGUIENTES(S)` | `{ $ }` | `{ $ }` | **✓ Coincide (100%)** |
| `SIGUIENTES(A..D)` | `{ cinco, cuatro, seis, tres, uno }` | `{ cinco, cuatro, seis, tres, uno }` | **✓ Coincide (100%)** |
| `PRED(Reglas 1-10)` | Idénticos regla por regla | Idénticos regla por regla | **✓ Coincide (100%)** |

---

## 4. ¿Qué significan estos resultados?

1. **Exactitud del Algoritmo:**  
   La equivalencia del 100% confirma la correcta implementación de la propagación transitiva y el tratamiento riguroso de la anulabilidad en secuencias donde múltiples símbolos intermedios derivan en $\varepsilon$.

2. **Diagnóstico de Gramática 1 (NO es LL(1)):**  
   - Presenta **recursión por la izquierda** directa en $S \to S \text{ dos}$ y $A \to A \text{ tres}$, lo cual provoca bucles infinitos en cualquier analizador descendente predictivo.
   - Presenta solapamientos severos en los conjuntos de predicción de $S$, $A$, $B$ y $D$.

3. **Diagnóstico de Gramática 2 (NO es LL(1)):**  
   - Aunque no tiene recursión izquierda y las alternativas de $A$ y $C$ son mutuamente disjuntas, **falla en $B$ y en $D$**:
     - $\text{PRED}(B \to CD) \cap \text{PRED}(B \to \varepsilon) = \{\text{cinco}, \text{cuatro}\} \ne \emptyset$.
     - $\text{PRED}(B \to \text{tres}) \cap \text{PRED}(B \to \varepsilon) = \{\text{tres}\} \ne \emptyset$.
     - $\text{PRED}(D \to \text{seis}) \cap \text{PRED}(D \to \varepsilon) = \{\text{seis}\} \ne \emptyset$.

4. **Impacto en el Análisis Sintáctico:**  
   En ninguna de las dos gramáticas un compilador descendente puede decidir determinísticamente qué producción aplicar utilizando solo 1 token de anticipación. Ambas requerirían reescritura de gramática (eliminación de recursión izquierda y factorización) antes de ser analizadas por un parser LL(1).

---

## 5. Referencias

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2007). *Compilers: Principles, Techniques, and Tools* (2.ª ed.). Pearson.
- Louden, K. C. (1997). *Compiler Construction: Principles and Practice*. PWS Publishing.
