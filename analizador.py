"""
Módulo: analizador.py
Implementación de los Algoritmos de:
1. PRIMEROS
2. SIGUIENTES
3. PREDICCIÓN
"""

import sys
import os
from typing import List, Set, Dict, Tuple

# Configurar salida UTF-8 en consola de Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

EPSILON = 'ε'
DOLLAR = '$'


class Produccion:
    """Representa una regla de producción A -> alpha."""
    def __init__(self, indice: int, izq: str, der: List[str]):
        self.indice = indice
        self.izq = izq
        self.der = der

    def __repr__(self):
        cuerpo = " ".join(self.der) if self.der else EPSILON
        return f"({self.indice}) {self.izq} -> {cuerpo}"


class Gramatica:
    """
    Carga y analiza una Gramática Libre de Contexto desde un archivo de texto (.txt).
    Implementa exclusivamente los algoritmos de PRIMEROS, SIGUIENTES y PREDICCIÓN.
    """
    def __init__(self, ruta_archivo: str = None):
        self.producciones: List[Produccion] = []
        self.no_terminales: List[str] = []
        self.terminales: List[str] = []
        self.simbolo_inicial: str = ""

        if ruta_archivo:
            self.cargar_desde_archivo(ruta_archivo)

    def cargar_desde_archivo(self, ruta_archivo: str):
        """Lee una gramática desde un archivo .txt con formato: A -> X1 X2 ..."""
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

        with open(ruta_archivo, 'r', encoding='utf-8-sig') as f:
            lineas_crudas = f.readlines()

        indice = 1
        no_term_set = set()
        cuerpos_tokens = []

        # Primera pasada: identificar producciones y no terminales
        for linea in lineas_crudas:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            if '->' not in linea:
                continue

            partes = linea.split('->')
            izq = partes[0].strip()
            der_str = partes[1].strip()

            if not self.simbolo_inicial:
                self.simbolo_inicial = izq

            no_term_set.add(izq)
            if izq not in self.no_terminales:
                self.no_terminales.append(izq)

            alternativas = der_str.split('|')
            for alt in alternativas:
                tokens = alt.strip().split()
                if not tokens or tokens == [EPSILON] or tokens == ['epsilon'] or tokens == ['EPS']:
                    tokens = [EPSILON]
                self.producciones.append(Produccion(indice, izq, tokens))
                cuerpos_tokens.append(tokens)
                indice += 1

        # Segunda pasada: identificar terminales
        term_set = set()
        for tokens in cuerpos_tokens:
            for t in tokens:
                if t != EPSILON and t not in no_term_set:
                    term_set.add(t)

        self.terminales = sorted(list(term_set))

    # =========================================================================
    # 1. ALGORITMO DE PRIMEROS
    # =========================================================================
    def primeros_de_secuencia(self, secuencia: List[str], primeros: Dict[str, Set[str]]) -> Set[str]:
        """
        Calcula PRIMEROS para una secuencia arbitraria X1 X2 ... Xk:
        PRIMEROS(X1...Xk) = U (PRIMEROS(Xi) - {ε}) hasta el primer Xi no anulable.
        Si todos los Xi son anulables (o secuencia vacía), incluye ε.
        """
        if not secuencia or secuencia == [EPSILON]:
            return {EPSILON}

        resultado: Set[str] = set()
        todos_anulables = True

        for simbolo in secuencia:
            if simbolo == EPSILON:
                continue
            elif simbolo in self.terminales:
                resultado.add(simbolo)
                todos_anulables = False
                break
            elif simbolo in self.no_terminales:
                prim_simbolo = primeros.get(simbolo, set())
                resultado.update(prim_simbolo - {EPSILON})
                if EPSILON not in prim_simbolo:
                    todos_anulables = False
                    break
            else:
                resultado.add(simbolo)
                todos_anulables = False
                break

        if todos_anulables:
            resultado.add(EPSILON)

        return resultado

    def calcular_primeros(self) -> Dict[str, Set[str]]:
        """
        Algoritmo de punto fijo para PRIMEROS(A) para cada no terminal A:
        1. Inicializar PRIMEROS(A) = ∅.
        2. Para cada regla A -> X1...Xk, agregar primeros_de_secuencia(X1...Xk).
        3. Repetir hasta alcanzar un punto fijo.
        """
        primeros: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}

        cambio = True
        while cambio:
            cambio = False
            for prod in self.producciones:
                nuevos = self.primeros_de_secuencia(prod.der, primeros)
                if not nuevos.issubset(primeros[prod.izq]):
                    primeros[prod.izq].update(nuevos)
                    cambio = True

        return primeros

    # =========================================================================
    # 2. ALGORITMO DE SIGUIENTES
    # =========================================================================
    def calcular_siguientes(self, primeros: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """
        Algoritmo de punto fijo para SIGUIENTES(A):
        1. Inicializar SIGUIENTES(S) = {$}.
        2. Para cada regla A -> alpha B beta:
           - Agregar (PRIMEROS(beta) - {ε}) a SIGUIENTES(B).
           - Si beta =>* ε (o beta vacía): agregar SIGUIENTES(A) a SIGUIENTES(B).
        3. Repetir hasta alcanzar punto fijo.
        """
        siguientes: Dict[str, Set[str]] = {nt: set() for nt in self.no_terminales}
        siguientes[self.simbolo_inicial].add(DOLLAR)

        cambio = True
        while cambio:
            cambio = False
            for prod in self.producciones:
                A = prod.izq
                cuerpo = prod.der
                for i, simbolo in enumerate(cuerpo):
                    if simbolo in self.no_terminales:
                        B = simbolo
                        beta = cuerpo[i + 1:]
                        prim_beta = self.primeros_de_secuencia(beta, primeros)

                        # Agregar PRIMEROS(beta) - {ε}
                        a_agregar = prim_beta - {EPSILON}
                        if not a_agregar.issubset(siguientes[B]):
                            siguientes[B].update(a_agregar)
                            cambio = True

                        # Si beta puede derivar en ε, propagar SIGUIENTES(A)
                        if EPSILON in prim_beta:
                            if not siguientes[A].issubset(siguientes[B]):
                                siguientes[B].update(siguientes[A])
                                cambio = True

        return siguientes

    # =========================================================================
    # 3. ALGORITMO DE PREDICCIÓN
    # =========================================================================
    def calcular_prediccion(self, primeros: Dict[str, Set[str]], siguientes: Dict[str, Set[str]]) -> List[Dict]:
        """
        Calcula el conjunto de PREDICCIÓN de cada regla A -> alpha:
        PRED(A -> alpha) =
           PRIMEROS(alpha)                          si ε ∉ PRIMEROS(alpha)
           (PRIMEROS(alpha) - {ε}) U SIGUIENTES(A)  si ε ∈ PRIMEROS(alpha)
        """
        predicciones = []
        for prod in self.producciones:
            prim_alpha = self.primeros_de_secuencia(prod.der, primeros)
            if EPSILON not in prim_alpha:
                conj_pred = set(prim_alpha)
            else:
                conj_pred = (prim_alpha - {EPSILON}) | siguientes[prod.izq]

            predicciones.append({
                'produccion': prod,
                'primeros_alpha': prim_alpha,
                'prediccion': conj_pred
            })

        return predicciones


def formatear_conjunto(s: Set[str]) -> str:
    """Formatea un conjunto de forma ordenada para impresión."""
    if not s:
        return "∅"
    items = sorted(list(s), key=lambda x: (x == EPSILON, x == DOLLAR, x))
    return "{ " + ", ".join(items) + " }"


def imprimir_analisis_completo(ruta_archivo: str, titulo: str = ""):
    print("\n" + "=" * 80)
    print(f"  {titulo.upper() or ruta_archivo}")
    print("=" * 80)

    g = Gramatica(ruta_archivo)

    print(f"\n1. GRAMÁTICA (cargada desde: {ruta_archivo}):")
    print(f"   No Terminales: {g.no_terminales}")
    print(f"   Terminales:    {g.terminales}")
    print(f"   Símbolo Inicial: {g.simbolo_inicial}\n")
    print("   Producciones:")
    for p in g.producciones:
        print(f"     {p}")

    # Ejecutar Algoritmo 1: PRIMEROS
    primeros = g.calcular_primeros()
    print("\n2. TABLA DE PRIMEROS:")
    print(f"   {'No Terminal':<15} | {'PRIMEROS':<40}")
    print("   " + "-" * 58)
    for nt in g.no_terminales:
        print(f"   {nt:<15} | {formatear_conjunto(primeros[nt]):<40}")

    # Ejecutar Algoritmo 2: SIGUIENTES
    siguientes = g.calcular_siguientes(primeros)
    print("\n3. TABLA DE SIGUIENTES:")
    print(f"   {'No Terminal':<15} | {'SIGUIENTES':<40}")
    print("   " + "-" * 58)
    for nt in g.no_terminales:
        print(f"   {nt:<15} | {formatear_conjunto(siguientes[nt]):<40}")

    # Ejecutar Algoritmo 3: PREDICCIÓN
    predicciones = g.calcular_prediccion(primeros, siguientes)
    print("\n4. TABLA DE PREDICCIÓN:")
    print(f"   {'Regla':<30} | {'PREDICCIÓN':<45}")
    print("   " + "-" * 78)
    for item in predicciones:
        prod = item['produccion']
        rule_str = f"({prod.indice}) {prod.izq} -> {' '.join(prod.der)}"
        print(f"   {rule_str:<30} | {formatear_conjunto(item['prediccion']):<45}")

    return g, primeros, siguientes, predicciones


def main():
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        imprimir_analisis_completo(ruta, f"ANÁLISIS DE {ruta}")
    else:
        # Por defecto ejecuta los dos ejercicios
        archivos = ["ejercicio1.txt", "ejercicio2.txt"]
        for idx, arch in enumerate(archivos, 1):
            if os.path.exists(arch):
                imprimir_analisis_completo(arch, f"EJERCICIO {idx} - GRAMÁTICA")
            else:
                print(f"No se encontró {arch}")


if __name__ == '__main__':
    main()
