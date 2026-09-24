# Algoritmos de Primeros, Siguientes y Predicción

**Asignatura:** Lenguajes de Programación y Transducción  
**Autor:** Dylan David Torres — [GitHub: @DylanDD17](https://github.com/DylanDD17)  
**Entorno:** Python 3.8+ (Biblioteca estándar)

---

## 1. ¿En qué consiste?

Este proyecto implementa en Python los algoritmos fundamentales del análisis sintáctico descendente:
1. **Algoritmo de PRIMEROS:** Determina el conjunto de terminales que pueden iniciar las cadenas derivadas por cada símbolo no terminal o secuencia.
2. **Algoritmo de SIGUIENTES:** Determina el conjunto de terminales (incluyendo el fin de entrada `$`) que pueden aparecer inmediatamente después de un no terminal en alguna derivación válida.
3. **Algoritmo de PREDICCIÓN:** Determina los tokens de anticipación (*lookahead*) válidos para elegir cada una de las reglas de producción.

El programa está diseñado de forma modular para cargar gramáticas libres de contexto directamente desde archivos de texto (`.txt`), ejecutar los algoritmos mediante cálculo de punto fijo, imprimir las tablas formateadas en consola y validar la equivalencia exacta con las deducciones analíticas de clase.

---

## 2. Archivos del Repositorio

* **`analizador.py`**: Código fuente principal en Python. Contiene el cargador de gramáticas desde archivos `.txt` y las funciones para calcular PRIMEROS, SIGUIENTES y PREDICCIÓN.
* **`ejercicio1.txt`**: Archivo de texto con las producciones de la gramática del Ejercicio 1.
* **`ejercicio2.txt`**: Archivo de texto con las producciones de la gramática del Ejercicio 2.
* **`capturas/`**: Carpeta con las capturas de imagen de la ejecución del analizador en terminal.
  * `salida_ejercicio1.png`: Captura de la ejecución del Ejercicio 1.
  * `salida_ejercicio2.png`: Captura de la ejecución del Ejercicio 2.
* **`README.md`**: Documento explicativo central del proyecto.
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

* **Python 3.8** o superior instalado en el sistema.
* No requiere la instalación de librerías externas o dependencias adicionales (utiliza únicamente módulos de la biblioteca estándar de Python).

---

## 5. Cómo Ejecutarlo

Para ejecutar el programa se utiliza la terminal o línea de comandos dentro del directorio del proyecto:

### Ejecutar ambos ejercicios automáticamente:
```bash
python analizador.py
```

### Ejecutar un archivo de gramática específico:
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
