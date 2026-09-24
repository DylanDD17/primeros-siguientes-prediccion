# Informe Académico: Algoritmos de Primeros, Siguientes y Predicción

**Asignatura:** Lenguajes de Programación y Transducción  
**Tema:** Análisis Sintáctico Descendente LL(1)  
**Autor:** Dylan David Torres (GitHub: [@DylanDD17](https://github.com/DylanDD17))  

---

## 1. Introducción y Objetivos

El análisis sintáctico descendente (*top-down parsing*) construye el árbol de derivación sintáctica desde la raíz (símbolo inicial) hacia las hojas mediante derivaciones por la izquierda (*leftmost derivations*). Para lograr que dicho análisis se ejecute de manera determinista y en tiempo lineal $\mathcal{O}(n)$, el analizador debe ser capaz de seleccionar la regla de producción correcta examinando únicamente el siguiente símbolo de entrada (*lookahead*).

Los objetivos de este trabajo son:
1. **Analíticamente**: Determinar rigurosamente los conjuntos de **PRIMEROS** (*FIRST*), **SIGUIENTES** (*FOLLOW*) de todos los no terminales, y **PREDICCIÓN** (*PREDICT*) de cada una de las reglas de producción para las dos gramáticas provistas.
2. **Computacionalmente**: Implementar en Python los algoritmos de punto fijo para el cálculo de PRIMEROS, SIGUIENTES y PREDICCIÓN, así como la construcción de la tabla predictiva $M[A, a]$ y detección de conflictos LL(1).
3. **Comparativamente**: Validar que los resultados computacionales coincidan al 100% con las derivaciones analíticas y diagnosticar el cumplimiento del criterio LL(1) en ambas gramáticas.

---

## 2. Marco Teórico y Fundamentos Matemáticos

De acuerdo con el material del curso (diapositivas de clase):

### 2.1. Símbolos y Secuencias Anulables
Un símbolo no terminal $X$ (o una secuencia $\alpha$) es **anulable** si puede derivar en la cadena vacía $\varepsilon$:
$$X \Rightarrow^* \varepsilon$$

### 2.2. Conjunto PRIMEROS
**Definición (Diapositiva 10):**
$$\text{PRIMEROS}(\alpha) = \{ a \in \Sigma \mid \alpha \Rightarrow^* a \beta \} \cup \{ \varepsilon \mid \alpha \Rightarrow^* \varepsilon \}$$

**Reglas de cálculo para una secuencia $X_1 X_2 \dots X_k$ (Diapositiva 11):**
1. Si $X_1$ es terminal, $\text{PRIMEROS}(X_1) = \{X_1\}$.
2. Para la secuencia, se agrega $(\text{PRIMEROS}(X_1) \setminus \{\varepsilon\})$.
3. Si $\varepsilon \in \text{PRIMEROS}(X_1)$, se continúa con $X_2$, y así sucesivamente hasta encontrar el primer símbolo no anulable.
4. Si todos los $X_i$ ($1 \le i \le k$) son anulables (o si la secuencia es vacía), se agrega $\varepsilon$.

$$\text{PRIMEROS}(X_1 \dots X_k) = \bigcup_{i=1}^{k} (\text{PRIMEROS}(X_i) \setminus \{\varepsilon\}) \quad \text{hasta el primer } X_i \text{ no anulable} \quad [\cup \{\varepsilon\} \text{ si todos son anulables}]$$

**Algoritmo de punto fijo (Diapositiva 14):**
Se inicializan $\text{PRIMEROS}(A) = \emptyset$ para todo $A \in V_N$, y se aplican iterativamente las reglas hasta que ningún conjunto cambie. La convergencia está garantizada por la monotonicidad y finitud del alfabeto.

### 2.3. Conjunto SIGUIENTES
**Definición (Diapositiva 15):**
$$\text{SIGUIENTES}(A) = \{ a \in \Sigma \cup \{\$\} \mid S \Rightarrow^* \mu A a \nu \}$$
Donde $\$$ representa el marcador de fin de entrada.

**Reglas de cálculo (Diapositiva 16):**
1. Inicializar $\$ \in \text{SIGUIENTES}(S)$, donde $S$ es el símbolo inicial.
2. Para cada producción de la forma $A \to \alpha B \beta$:
   - Agregar $(\text{PRIMEROS}(\beta) \setminus \{\varepsilon\})$ a $\text{SIGUIENTES}(B)$.
   - Si $\beta \Rightarrow^* \varepsilon$ (es decir, $\varepsilon \in \text{PRIMEROS}(\beta)$ o $\beta$ es vacía), agregar $\text{SIGUIENTES}(A)$ a $\text{SIGUIENTES}(B)$.
3. Repetir hasta alcanzar el punto fijo.
4. **Cuidado:** $\varepsilon$ nunca pertenece a un conjunto $\text{SIGUIENTES}$.

### 2.4. Conjunto de PREDICCIÓN de una Producción
**Definición (Diapositiva 18):**
Para una producción $A \to \alpha$:
$$\text{PRED}(A \to \alpha) = \begin{cases} \text{PRIMEROS}(\alpha), & \text{si } \varepsilon \notin \text{PRIMEROS}(\alpha) \\ (\text{PRIMEROS}(\alpha) \setminus \{\varepsilon\}) \cup \text{SIGUIENTES}(A), & \text{si } \varepsilon \in \text{PRIMEROS}(\alpha) \end{cases}$$

### 2.5. Criterio LL(1) y Tabla de Análisis
**Criterio (Diapositiva 9 y 25):**
Una gramática es LL(1) si y solo si para cada no terminal $A$, todas sus producciones alternativas tienen conjuntos de predicción mutuamente disjuntos:
$$\forall (A \to \alpha), (A \to \beta) \text{ con } \alpha \ne \beta : \quad \text{PRED}(A \to \alpha) \cap \text{PRED}(A \to \beta) = \emptyset$$

---

## 3. Ejercicio 1: Análisis Detallado de la Gramática 1

### 3.1. Definición de la Gramática
- **No terminales:** $V_N = \{S, A, B, C, D\}$
- **Terminales:** $V_T = \{\text{uno, dos, tres, cuatro, cinco, seis}\}$
- **Símbolo inicial:** $S$
- **Reglas de producción:**
  1. $S \to A \text{ uno } B C$
  2. $S \to S \text{ dos}$
  3. $A \to B C D$
  4. $A \to A \text{ tres}$
  5. $A \to \varepsilon$
  6. $B \to D \text{ cuatro } C \text{ tres}$
  7. $B \to \varepsilon$
  8. $C \to \text{cinco } D B$
  9. $C \to \varepsilon$
  10. $D \to \text{seis}$
  11. $D \to \varepsilon$

### 3.2. Análisis de Anulabilidad
- $D \to \varepsilon \implies D$ es anulable ($\varepsilon \in \text{PRIMEROS}(D)$).
- $C \to \varepsilon \implies C$ es anulable ($\varepsilon \in \text{PRIMEROS}(C)$).
- $B \to \varepsilon \implies B$ es anulable ($\varepsilon \in \text{PRIMEROS}(B)$).
- $A \to \varepsilon \implies A$ es anulable ($\varepsilon \in \text{PRIMEROS}(A)$).
- $S \to A \text{ uno } B C$ contiene el terminal 'uno'; $S \to S \text{ dos}$ termina en 'dos'. Por tanto, $S$ **no es anulable** ($\varepsilon \notin \text{PRIMEROS}(S)$).

### 3.3. Cálculo Analítico de PRIMEROS
Aplicamos el algoritmo de punto fijo:

- **Para $D$:**
  - $D \to \text{seis} \implies \text{seis} \in \text{PRIMEROS}(D)$.
  - $D \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(D)$.
  - **$\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$**.

- **Para $C$:**
  - $C \to \text{cinco } D B \implies \text{cinco} \in \text{PRIMEROS}(C)$.
  - $C \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(C)$.
  - **$\text{PRIMEROS}(C) = \{\text{cinco}, \varepsilon\}$**.

- **Para $B$:**
  - $B \to D \text{ cuatro } C \text{ tres}$:
    Como $\varepsilon \in \text{PRIMEROS}(D)$, tomamos $(\text{PRIMEROS}(D) \setminus \{\varepsilon\}) \cup \text{PRIMEROS}(\text{cuatro}) = \{\text{seis}\} \cup \{\text{cuatro}\} = \{\text{cuatro}, \text{seis}\}$.
  - $B \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(B)$.
  - **$\text{PRIMEROS}(B) = \{\text{cuatro}, \text{seis}, \varepsilon\}$**.

- **Para $A$:**
  - $A \to B C D$:
    Dado que $B, C, D$ son anulables:
    $(\text{PRIMEROS}(B) \setminus \{\varepsilon\}) \cup (\text{PRIMEROS}(C) \setminus \{\varepsilon\}) \cup (\text{PRIMEROS}(D) \setminus \{\varepsilon\}) \cup \{\varepsilon\}$
    $= \{\text{cuatro}, \text{seis}\} \cup \{\text{cinco}\} \cup \{\text{seis}\} \cup \{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \varepsilon\}$.
  - $A \to A \text{ tres}$:
    Como $A \Rightarrow^* \varepsilon$, se puede derivar $A \Rightarrow A \text{ tres} \Rightarrow \varepsilon \text{ tres} = \text{tres}$. Por ende, $\text{tres} \in \text{PRIMEROS}(A)$.
  - $A \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(A)$.
  - **$\text{PRIMEROS}(A) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$**.

- **Para $S$:**
  - $S \to A \text{ uno } B C$:
    Como $\varepsilon \in \text{PRIMEROS}(A)$, toma $(\text{PRIMEROS}(A) \setminus \{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$.
  - $S \to S \text{ dos}$: Agrega $(\text{PRIMEROS}(S) \setminus \{\varepsilon\})$, que no añade nuevos símbolos.
  - **$\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$**.

---

### 3.4. Cálculo Analítico de SIGUIENTES
1. **Inicialización:**
   $\text{SIGUIENTES}(S) = \{\$\}$.

2. **Propagación según las producciones:**
   - **De la regla (2) $S \to S \text{ dos}$:**
     $S$ va seguido del terminal 'dos' $\implies \text{dos} \in \text{SIGUIENTES}(S)$.
     Por tanto: **$\text{SIGUIENTES}(S) = \{\text{dos}, \$\}$**.
   - **De la regla (1) $S \to A \text{ uno } B C$:**
     - $A$ va seguido de 'uno' $\implies \text{uno} \in \text{SIGUIENTES}(A)$.
     - $B$ va seguido de $C \implies \text{PRIMEROS}(C) \setminus \{\varepsilon\} = \{\text{cinco}\} \subseteq \text{SIGUIENTES}(B)$.
       Como $C \Rightarrow^* \varepsilon$, $\text{SIGUIENTES}(S) \subseteq \text{SIGUIENTES}(B)$.
     - $C$ está al final de la producción $\implies \text{SIGUIENTES}(S) \subseteq \text{SIGUIENTES}(C)$.
   - **De la regla (4) $A \to A \text{ tres}$:**
     $A$ va seguido de 'tres' $\implies \text{tres} \in \text{SIGUIENTES}(A)$.
     Por tanto: **$\text{SIGUIENTES}(A) = \{\text{tres}, \text{uno}\}$**.
   - **De la regla (3) $A \to B C D$:**
     - $B$ va seguido de $C D \implies \text{PRIMEROS}(C D) \setminus \{\varepsilon\} = \{\text{cinco}, \text{seis}\} \subseteq \text{SIGUIENTES}(B)$.
       Como $C D \Rightarrow^* \varepsilon$, $\text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(B)$.
     - $C$ va seguido de $D \implies \text{PRIMEROS}(D) \setminus \{\varepsilon\} = \{\text{seis}\} \subseteq \text{SIGUIENTES}(C)$.
       Como $D \Rightarrow^* \varepsilon$, $\text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(C)$.
     - $D$ está al final de la producción $\implies \text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(D)$.
   - **De la regla (6) $B \to D \text{ cuatro } C \text{ tres}$:**
     - $D$ va seguido de 'cuatro' $\implies \text{cuatro} \in \text{SIGUIENTES}(D)$.
     - $C$ va seguido de 'tres' $\implies \text{tres} \in \text{SIGUIENTES}(C)$.
   - **De la regla (8) $C \to \text{cinco } D B$:**
     - $D$ va seguido de $B \implies \text{PRIMEROS}(B) \setminus \{\varepsilon\} = \{\text{cuatro}, \text{seis}\} \subseteq \text{SIGUIENTES}(D)$.
       Como $B \Rightarrow^* \varepsilon$, $\text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(D)$.
     - $B$ está al final $\implies \text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(B)$.

3. **Cierre de punto fijo:**
   - $\text{SIGUIENTES}(C) = \text{SIGUIENTES}(S) \cup \{\text{seis}\} \cup \text{SIGUIENTES}(A) \cup \{\text{tres}\}$  
     $= \{\text{dos}, \$\} \cup \{\text{seis}\} \cup \{\text{tres}, \text{uno}\} \cup \{\text{tres}\} = \mathbf{\{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}}$.
   - $\text{SIGUIENTES}(B) = \text{SIGUIENTES}(C) \cup \{\text{cinco}\} = \mathbf{\{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}}$.
   - $\text{SIGUIENTES}(D) = \{\text{cuatro}\} \cup \text{SIGUIENTES}(A) \cup \{\text{cuatro}, \text{seis}\} \cup \text{SIGUIENTES}(C) = \mathbf{\{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}}$.

---

### 3.5. Cálculo Analítico de PREDICCIÓN (Gramática 1)

| Regla | Producción $A \to \alpha$ | $\text{PRIMEROS}(\alpha)$ | ¿$\alpha \Rightarrow^* \varepsilon$? | Fórmula Aplicada | $\text{PRED}(A \to \alpha)$ |
|:---:|:---|:---|:---:|:---|:---|
| **(1)** | $S \to A \text{ uno } B C$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **(2)** | $S \to S \text{ dos}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **(3)** | $A \to B C D$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \varepsilon\}$ | **Sí** | $(\text{PRIMEROS} \setminus \{\varepsilon\}) \cup \text{SIG}(A)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **(4)** | $A \to A \text{ tres}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}\}$ |
| **(5)** | $A \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(A)$ | $\{\text{tres}, \text{uno}\}$ |
| **(6)** | $B \to D \text{ cuatro } C \text{ tres}$ | $\{\text{cuatro}, \text{seis}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cuatro}, \text{seis}\}$ |
| **(7)** | $B \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(B)$ | $\{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ |
| **(8)** | $C \to \text{cinco } D B$ | $\{\text{cinco}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}\}$ |
| **(9)** | $C \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(C)$ | $\{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ |
| **(10)**| $D \to \text{seis}$ | $\{\text{seis}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{seis}\}$ |
| **(11)**| $D \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(D)$ | $\{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ |

---

## 4. Ejercicio 2: Análisis Detallado de la Gramática 2

### 4.1. Definición de la Gramática
- **No terminales:** $V_N = \{S, A, B, C, D\}$
- **Terminales:** $V_T = \{\text{uno, dos, tres, cuatro, cinco, seis}\}$
- **Símbolo inicial:** $S$
- **Reglas de producción:**
  1. $S \to A B \text{ uno}$
  2. $A \to \text{dos } B$
  3. $A \to \varepsilon$
  4. $B \to C D$
  5. $B \to \text{tres}$
  6. $B \to \varepsilon$
  7. $C \to \text{cuatro } A B$
  8. $C \to \text{cinco}$
  9. $D \to \text{seis}$
  10. $D \to \varepsilon$

### 4.2. Análisis de Anulabilidad
- $A \to \varepsilon \implies A$ es anulable ($\varepsilon \in \text{PRIMEROS}(A)$).
- $D \to \varepsilon \implies D$ es anulable ($\varepsilon \in \text{PRIMEROS}(D)$).
- $B \to \varepsilon \implies B$ es anulable ($\varepsilon \in \text{PRIMEROS}(B)$).
- $C$: Las producciones de $C$ inician con terminales ('cuatro', 'cinco'). $C$ **no es anulable** ($\varepsilon \notin \text{PRIMEROS}(C)$).
- Como $C$ no es anulable, la regla $B \to C D$ no deriva en $\varepsilon$, pero $B$ sigue siendo anulable gracias a $B \to \varepsilon$.
- $S \to A B \text{ uno}$: termina en el terminal 'uno', por lo que $S$ **no es anulable**.

### 4.3. Cálculo Analítico de PRIMEROS
- **Para $D$:**
  - $D \to \text{seis} \implies \text{seis} \in \text{PRIMEROS}(D)$.
  - $D \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(D)$.
  - **$\text{PRIMEROS}(D) = \{\text{seis}, \varepsilon\}$**.

- **Para $C$:**
  - $C \to \text{cuatro } A B \implies \text{cuatro} \in \text{PRIMEROS}(C)$.
  - $C \to \text{cinco} \implies \text{cinco} \in \text{PRIMEROS}(C)$.
  - **$\text{PRIMEROS}(C) = \{\text{cuatro}, \text{cinco}\}$**.

- **Para $B$:**
  - $B \to C D$: Como $\varepsilon \notin \text{PRIMEROS}(C)$, la secuencia se detiene en $C$. Aporta $\text{PRIMEROS}(C) = \{\text{cuatro}, \text{cinco}\}$.
  - $B \to \text{tres} \implies \text{tres} \in \text{PRIMEROS}(B)$.
  - $B \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(B)$.
  - **$\text{PRIMEROS}(B) = \{\text{cinco}, \text{cuatro}, \text{tres}, \varepsilon\}$**.

- **Para $A$:**
  - $A \to \text{dos } B \implies \text{dos} \in \text{PRIMEROS}(A)$.
  - $A \to \varepsilon \implies \varepsilon \in \text{PRIMEROS}(A)$.
  - **$\text{PRIMEROS}(A) = \{\text{dos}, \varepsilon\}$**.

- **Para $S$:**
  - $S \to A B \text{ uno}$:
    - Como $A \Rightarrow^* \varepsilon$, agrega $\text{PRIMEROS}(A) \setminus \{\varepsilon\} = \{\text{dos}\}$.
    - Continúa con $B$: agrega $\text{PRIMEROS}(B) \setminus \{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{tres}\}$.
    - Como $B \Rightarrow^* \varepsilon$, continúa con 'uno': agrega $\{\text{uno}\}$.
  - **$\text{PRIMEROS}(S) = \{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$**.

---

### 4.4. Cálculo Analítico de SIGUIENTES
1. **Inicialización:**
   $\text{SIGUIENTES}(S) = \{\$\}$.

2. **Propagación según las producciones:**
   - **De la regla (1) $S \to A B \text{ uno}$:**
     - $A$ va seguido de $B \text{ uno}$:
       $\text{PRIMEROS}(B \text{ uno}) = (\text{PRIMEROS}(B) \setminus \{\varepsilon\}) \cup \{\text{uno}\} = \{\text{cinco}, \text{cuatro}, \text{tres}, \text{uno}\}$.
       Por lo tanto: $\{\text{cinco}, \text{cuatro}, \text{tres}, \text{uno}\} \subseteq \text{SIGUIENTES}(A)$.
     - $B$ va seguido de 'uno' $\implies \text{uno} \in \text{SIGUIENTES}(B)$.
     - $S$ no aparece a la derecha de ninguna producción $\implies \text{SIGUIENTES}(S) = \mathbf{\{\$\}}$.
   - **De la regla (2) $A \to \text{dos } B$:**
     - $B$ queda al final de la producción $\implies \text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(B)$.
   - **De la regla (4) $B \to C D$:**
     - $C$ va seguido de $D \implies \text{PRIMEROS}(D) \setminus \{\varepsilon\} = \{\text{seis}\} \subseteq \text{SIGUIENTES}(C)$.
       Como $D \Rightarrow^* \varepsilon$, $\text{SIGUIENTES}(B) \subseteq \text{SIGUIENTES}(C)$.
     - $D$ queda al final $\implies \text{SIGUIENTES}(B) \subseteq \text{SIGUIENTES}(D)$.
   - **De la regla (7) $C \to \text{cuatro } A B$:**
     - $A$ va seguido de $B \implies \text{PRIMEROS}(B) \setminus \{\varepsilon\} = \{\text{cinco}, \text{cuatro}, \text{tres}\} \subseteq \text{SIGUIENTES}(A)$.
       Como $B \Rightarrow^* \varepsilon$, $\text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(A)$.
     - $B$ queda al final $\implies \text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(B)$.

3. **Cierre de punto fijo:**
   Observemos el ciclo de inclusión mutua:
   $$\text{SIGUIENTES}(A) \subseteq \text{SIGUIENTES}(B) \subseteq \text{SIGUIENTES}(C) \subseteq \text{SIGUIENTES}(A)$$
   Esto implica que los tres conjuntos deben converger exactamente al mismo conjunto:
   - Partiendo de $\text{SIGUIENTES}(A) \supseteq \{\text{cinco}, \text{cuatro}, \text{tres}, \text{uno}\}$.
   - Fluye a $B$: $\text{SIGUIENTES}(B) \supseteq \{\text{cinco}, \text{cuatro}, \text{tres}, \text{uno}\}$.
   - Fluye a $C$, sumando además $\{\text{seis}\}$ proveniente de $D$:
     $\text{SIGUIENTES}(C) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$.
   - Fluye de regreso a $B$ y luego a $A$:
     Ambos incorporan $\{\text{seis}\}$.
   - Finalmente, $D$ recibe $\text{SIGUIENTES}(B)$:
     $\text{SIGUIENTES}(D) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$.

   **Resultado final de SIGUIENTES:**
   - $\text{SIGUIENTES}(S) = \mathbf{\{\$\}}$
   - $\text{SIGUIENTES}(A) = \mathbf{\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}}$
   - $\text{SIGUIENTES}(B) = \mathbf{\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}}$
   - $\text{SIGUIENTES}(C) = \mathbf{\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}}$
   - $\text{SIGUIENTES}(D) = \mathbf{\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}}$

---

### 4.5. Cálculo Analítico de PREDICCIÓN (Gramática 2)

| Regla | Producción $A \to \alpha$ | $\text{PRIMEROS}(\alpha)$ | ¿$\alpha \Rightarrow^* \varepsilon$? | Fórmula Aplicada | $\text{PRED}(A \to \alpha)$ |
|:---:|:---|:---|:---:|:---|:---|
| **(1)** | $S \to A B \text{ uno}$ | $\{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$ |
| **(2)** | $A \to \text{dos } B$ | $\{\text{dos}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{dos}\}$ |
| **(3)** | $A \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(A)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **(4)** | $B \to C D$ | $\{\text{cinco}, \text{cuatro}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}, \text{cuatro}\}$ |
| **(5)** | $B \to \text{tres}$ | $\{\text{tres}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{tres}\}$ |
| **(6)** | $B \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(B)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |
| **(7)** | $C \to \text{cuatro } A B$ | $\{\text{cuatro}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cuatro}\}$ |
| **(8)** | $C \to \text{cinco}$ | $\{\text{cinco}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{cinco}\}$ |
| **(9)** | $D \to \text{seis}$ | $\{\text{seis}\}$ | No | $\text{PRIMEROS}(\alpha)$ | $\{\text{seis}\}$ |
| **(10)**| $D \to \varepsilon$ | $\{\varepsilon\}$ | **Sí** | $\text{SIGUIENTES}(D)$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ |

---

## 5. Tablas Comparativas: Analítico vs. Computacional

### 5.1. Comparación para Gramática 1

#### PRIMEROS:
| No Terminal | Analítico | Computacional | Coincidencia |
|:---:|:---|:---|:---:|
| $S$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | **100% Exacto** |
| $A$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \varepsilon\}$ | **100% Exacto** |
| $B$ | $\{\text{cuatro}, \text{seis}, \varepsilon\}$ | $\{\text{cuatro}, \text{seis}, \varepsilon\}$ | **100% Exacto** |
| $C$ | $\{\text{cinco}, \varepsilon\}$ | $\{\text{cinco}, \varepsilon\}$ | **100% Exacto** |
| $D$ | $\{\text{seis}, \varepsilon\}$ | $\{\text{seis}, \varepsilon\}$ | **100% Exacto** |

#### SIGUIENTES:
| No Terminal | Analítico | Computacional | Coincidencia |
|:---:|:---|:---|:---:|
| $S$ | $\{\text{dos}, \$\}$ | $\{\text{dos}, \$\}$ | **100% Exacto** |
| $A$ | $\{\text{tres}, \text{uno}\}$ | $\{\text{tres}, \text{uno}\}$ | **100% Exacto** |
| $B$ | $\{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ | $\{\text{cinco}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ | **100% Exacto** |
| $C$ | $\{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ | $\{\text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ | **100% Exacto** |
| $D$ | $\{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ | $\{\text{cuatro}, \text{dos}, \text{seis}, \text{tres}, \text{uno}, \$\}$ | **100% Exacto** |

#### PREDICCIÓN:
Todas las 11 reglas de la Gramática 1 presentan coincidencia total del 100% entre la deducción analítica y la ejecución del script Python.

---

### 5.2. Comparación para Gramática 2

#### PRIMEROS:
| No Terminal | Analítico | Computacional | Coincidencia |
|:---:|:---|:---|:---:|
| $S$ | $\{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$ | $\{\text{cinco}, \text{cuatro}, \text{dos}, \text{tres}, \text{uno}\}$ | **100% Exacto** |
| $A$ | $\{\text{dos}, \varepsilon\}$ | $\{\text{dos}, \varepsilon\}$ | **100% Exacto** |
| $B$ | $\{\text{cinco}, \text{cuatro}, \text{tres}, \varepsilon\}$ | $\{\text{cinco}, \text{cuatro}, \text{tres}, \varepsilon\}$ | **100% Exacto** |
| $C$ | $\{\text{cinco}, \text{cuatro}\}$ | $\{\text{cinco}, \text{cuatro}\}$ | **100% Exacto** |
| $D$ | $\{\text{seis}, \varepsilon\}$ | $\{\text{seis}, \varepsilon\}$ | **100% Exacto** |

#### SIGUIENTES:
| No Terminal | Analítico | Computacional | Coincidencia |
|:---:|:---|:---|:---:|
| $S$ | $\{\$\}$ | $\{\$\}$ | **100% Exacto** |
| $A$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | **100% Exacto** |
| $B$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | **100% Exacto** |
| $C$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | **100% Exacto** |
| $D$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | $\{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\}$ | **100% Exacto** |

#### PREDICCIÓN:
Las 10 reglas de la Gramática 2 presentan coincidencia total del 100% con los cálculos del script de Python.

---

## 6. Diagnóstico LL(1) y Discusión de Conflictos

De acuerdo con la **Diapositiva 25 (¿Cuándo una gramática no es LL(1)?):**
- **Gramática 1:**
  1. Presenta **recursión por la izquierda directa** en dos no terminales:
     - $S \to S \text{ dos}$ (hace imposible el descenso recursivo sin bucle infinito).
     - $A \to A \text{ tres}$.
  2. Sus alternativas comparten tokens de predicción:
     - $\text{PRED}(S \to A \text{ uno } B C) \cap \text{PRED}(S \to S \text{ dos}) = \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\} \ne \emptyset$.
     - $\text{PRED}(A \to B C D) \cap \text{PRED}(A \to A \text{ tres}) \ne \emptyset$.
     - $\text{PRED}(B \to D \text{ cuatro } C \text{ tres}) \cap \text{PRED}(B \to \varepsilon) = \{\text{cuatro}, \text{seis}\} \ne \emptyset$.
     - $\text{PRED}(D \to \text{seis}) \cap \text{PRED}(D \to \varepsilon) = \{\text{seis}\} \ne \emptyset$.
  - **Conclusión:** La Gramática 1 **NO es LL(1)**.

- **Gramática 2:**
  1. No tiene recursión por la izquierda.
  2. Las alternativas de $A$ y de $C$ son perfectamente disjuntas:
     - $\text{PRED}(A \to \text{dos } B) \cap \text{PRED}(A \to \varepsilon) = \{\text{dos}\} \cap \{\text{cinco}, \text{cuatro}, \text{seis}, \text{tres}, \text{uno}\} = \emptyset$.
     - $\text{PRED}(C \to \text{cuatro } A B) \cap \text{PRED}(C \to \text{cinco}) = \{\text{cuatro}\} \cap \{\text{cinco}\} = \emptyset$.
  3. Sin embargo, aparecen conflictos de predicción en $B$ y $D$:
     - Para $B$: $\text{PRED}(B \to C D) \cap \text{PRED}(B \to \varepsilon) = \{\text{cinco}, \text{cuatro}\} \ne \emptyset$.
     - Para $B$: $\text{PRED}(B \to \text{tres}) \cap \text{PRED}(B \to \varepsilon) = \{\text{tres}\} \ne \emptyset$.
     - Para $D$: $\text{PRED}(D \to \text{seis}) \cap \text{PRED}(D \to \varepsilon) = \{\text{seis}\} \ne \emptyset$.
  - **Conclusión:** La Gramática 2 **NO es LL(1)**. Al construir la tabla predictiva $M$, las celdas $M[B, \text{tres}]$, $M[B, \text{cuatro}]$, $M[B, \text{cinco}]$ y $M[D, \text{seis}]$ contienen más de una regla de producción.

---

## 7. Referencias Bibliográficas

- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2007). *Compilers: Principles, Techniques, and Tools* (2.ª ed.). Pearson.
- Grune, D., & Jacobs, C. J. H. (2008). *Parsing Techniques: A Practical Guide* (2.ª ed.). Springer.
- Parr, T. (2013). *The Definitive ANTLR 4 Reference*. Pragmatic Bookshelf.
- Louden, K. C. (1997). *Compiler Construction: Principles and Practice*. PWS Publishing.
