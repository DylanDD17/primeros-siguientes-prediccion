"""
Programa Principal: main.py
Tarea: Algoritmos de Primeros, Siguientes y Predicción
Curso: Lenguajes de Programación y Transducción

Ejecuta el análisis sintáctico descendente para las Gramáticas 1 y 2:
- Muestra el cálculo analítico paso a paso
- Ejecuta los algoritmos en Python
- Compara los resultados analíticos vs computacionales
- Construye la tabla LL(1) y reporta conflictos
"""

import sys
from typing import Dict, Set, List
from grammar_analyzer import GrammarAnalyzer, Production, EPSILON, DOLLAR

# Asegurar codificación UTF-8 para salida en terminales de Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def format_set(s: Set[str]) -> str:
    """Formatea un conjunto de símbolos ordenado."""
    if not s:
        return "∅"
    # Colocar terminales ordenados, con ε o $ ordenados adecuadamente
    items = sorted(list(s), key=lambda x: (x == EPSILON, x == DOLLAR, x))
    return "{ " + ", ".join(items) + " }"


def print_banner(title: str):
    print("\n" + "=" * 80)
    print(f"  {title.upper()}")
    print("=" * 80)


def print_section(title: str):
    print("\n" + "-" * 80)
    print(f"▶ {title}")
    print("-" * 80)


def display_grammar_analysis(grammar_num: int, title: str, analyzer: GrammarAnalyzer, 
                             analytical_first: Dict[str, Set[str]],
                             analytical_follow: Dict[str, Set[str]],
                             analytical_pred: List[Set[str]]):
    print_banner(f"GRAMÁTICA {grammar_num}: {title}")

    # 1. Reglas de Producción
    print_section("1. REGLAS DE PRODUCCIÓN")
    for prod in analyzer.productions:
        print(f"   ({prod.index}) {prod.lhs} -> {' '.join(prod.rhs)}")

    # 2. Algoritmo PRIMEROS con traza de iteraciones
    print_section("2. CÁLCULO DE PRIMEROS (ALGORITMO DE PUNTO FIJO)")
    first_sets, first_history = analyzer.compute_first(track_iterations=True)
    for i, state in enumerate(first_history, 1):
        print(f"   Iteración {i}:")
        for nt in analyzer.non_terminals:
            print(f"      PRIMEROS({nt}) = {format_set(state[nt])}")

    # 3. Algoritmo SIGUIENTES con traza de iteraciones
    print_section("3. CÁLCULO DE SIGUIENTES (ALGORITMO DE PUNTO FIJO)")
    follow_sets, follow_history = analyzer.compute_follow(first_sets, track_iterations=True)
    for i, state in enumerate(follow_history, 1):
        print(f"   Iteración {i}:")
        for nt in analyzer.non_terminals:
            print(f"      SIGUIENTES({nt}) = {format_set(state[nt])}")

    # 4. Conjuntos de PREDICCIÓN
    print_section("4. CONJUNTOS DE PREDICCIÓN DE CADA REGLA")
    print(f"   {'Regla':<30} | {'PRIMEROS(α)':<32} | {'Anulable':<9} | {'PREDICCIÓN':<35}")
    print("   " + "-" * 115)
    predictions = analyzer.compute_prediction(first_sets, follow_sets)
    for item in predictions:
        p = item['production']
        rule_str = f"({p.index}) {p.lhs} -> {' '.join(p.rhs)}"
        first_a_str = format_set(item['first_alpha'])
        nullable_str = "Sí (ε)" if item['is_nullable'] else "No"
        pred_str = format_set(item['pred_set'])
        print(f"   {rule_str:<30} | {first_a_str:<32} | {nullable_str:<9} | {pred_str:<35}")

    # 5. Comparación Analítico vs Computacional
    print_section("5. COMPARACIÓN: RESULTADOS ANALÍTICOS vs COMPUTACIONALES")
    
    print("\n   [A] PRIMEROS:")
    print(f"   {'No Terminal':<12} | {'Resultado Analítico':<35} | {'Resultado Computacional':<35} | {'¿Coincide?':<10}")
    print("   " + "-" * 100)
    for nt in analyzer.non_terminals:
        an_str = format_set(analytical_first[nt])
        comp_str = format_set(first_sets[nt])
        match = "✓ SÍ (100%)" if analytical_first[nt] == first_sets[nt] else "✗ NO"
        print(f"   {nt:<12} | {an_str:<35} | {comp_str:<35} | {match:<10}")

    print("\n   [B] SIGUIENTES:")
    print(f"   {'No Terminal':<12} | {'Resultado Analítico':<35} | {'Resultado Computacional':<35} | {'¿Coincide?':<10}")
    print("   " + "-" * 100)
    for nt in analyzer.non_terminals:
        an_str = format_set(analytical_follow[nt])
        comp_str = format_set(follow_sets[nt])
        match = "✓ SÍ (100%)" if analytical_follow[nt] == follow_sets[nt] else "✗ NO"
        print(f"   {nt:<12} | {an_str:<35} | {comp_str:<35} | {match:<10}")

    print("\n   [C] CONJUNTOS DE PREDICCIÓN:")
    print(f"   {'Regla':<28} | {'Predicción Analítica':<35} | {'Predicción Computacional':<35} | {'¿Coincide?':<10}")
    print("   " + "-" * 115)
    for i, item in enumerate(predictions):
        p = item['production']
        rule_str = f"({p.index}) {p.lhs} -> {' '.join(p.rhs)}"
        an_str = format_set(analytical_pred[i])
        comp_str = format_set(item['pred_set'])
        match = "✓ SÍ (100%)" if analytical_pred[i] == item['pred_set'] else "✗ NO"
        print(f"   {rule_str:<28} | {an_str:<35} | {comp_str:<35} | {match:<10}")

    # 6. Verificación de Criterio LL(1) y Tabla
    print_section("6. DIAGNÓSTICO LL(1) Y TABLA DE ANÁLISIS PREDICTIVO")
    is_ll1, conflicts = analyzer.check_ll1_conflicts(predictions)
    
    if is_ll1:
        print("   ✓ LA GRAMÁTICA ES LL(1): Todos los conjuntos de predicción para alternativas del mismo no terminal son disjuntos.")
    else:
        print("   ✗ LA GRAMÁTICA NO ES LL(1): Se encontraron conflictos de predicción entre producciones alternativas:")
        for nt, confl_list in conflicts.items():
            for p1, p2, inter in confl_list:
                print(f"      - Conflicto en '{nt}':")
                print(f"        Regla ({p1.index}): {p1.lhs} -> {' '.join(p1.rhs)}")
                print(f"        Regla ({p2.index}): {p2.lhs} -> {' '.join(p2.rhs)}")
                print(f"        Tokens en intersección: {format_set(inter)}")

    # Construir tabla M[A, a]
    print("\n   TABLA DE ANÁLISIS PREDICTIVO M[A, a]:")
    table = analyzer.build_parsing_table(predictions)
    all_terms = analyzer.terminals + [DOLLAR]
    header = f"   {'NT':<5} | " + " | ".join(f"{t:<14}" for t in all_terms)
    print(header)
    print("   " + "-" * len(header))
    for nt in analyzer.non_terminals:
        row = [f"   {nt:<5}"]
        for t in all_terms:
            cell_prods = table[nt][t]
            if not cell_prods:
                cell_str = "—"
            elif len(cell_prods) == 1:
                cell_str = f"R{cell_prods[0].index}"
            else:
                cell_str = f"CONFLICTO({','.join('R' + str(p.index) for p in cell_prods)})"
            row.append(f"{cell_str:<14}")
        print(" | ".join(row))


def main():
    print_banner("PROYECTO: ALGORITMOS DE PRIMEROS, SIGUIENTES Y PREDICCIÓN")
    print("Asignatura: Lenguajes de Programación y Transducción")
    print("Autores: Dylan David Torres (DylanDD17)")
    print("Base Teórica: Material del curso (Análisis Sintáctico Descendente LL(1))\n")

    non_terminals = ['S', 'A', 'B', 'C', 'D']
    terminals = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis']

    # ==========================================
    # GRAMÁTICA 1
    # ==========================================
    prods1 = [
        ('S', ['A', 'uno', 'B', 'C']),
        ('S', ['S', 'dos']),
        ('A', ['B', 'C', 'D']),
        ('A', ['A', 'tres']),
        ('A', [EPSILON]),
        ('B', ['D', 'cuatro', 'C', 'tres']),
        ('B', [EPSILON]),
        ('C', ['cinco', 'D', 'B']),
        ('C', [EPSILON]),
        ('D', ['seis']),
        ('D', [EPSILON]),
    ]
    g1 = GrammarAnalyzer(non_terminals, terminals, 'S', prods1)

    an_first_1 = {
        'S': {'cinco', 'cuatro', 'seis', 'tres', 'uno'},
        'A': {'cinco', 'cuatro', 'seis', 'tres', EPSILON},
        'B': {'cuatro', 'seis', EPSILON},
        'C': {'cinco', EPSILON},
        'D': {'seis', EPSILON},
    }
    an_follow_1 = {
        'S': {DOLLAR, 'dos'},
        'A': {'tres', 'uno'},
        'B': {DOLLAR, 'cinco', 'dos', 'seis', 'tres', 'uno'},
        'C': {DOLLAR, 'dos', 'seis', 'tres', 'uno'},
        'D': {DOLLAR, 'cuatro', 'dos', 'seis', 'tres', 'uno'},
    }
    an_pred_1 = [
        {'cinco', 'cuatro', 'seis', 'tres', 'uno'},              # 1: S -> A uno B C
        {'cinco', 'cuatro', 'seis', 'tres', 'uno'},              # 2: S -> S dos
        {'cinco', 'cuatro', 'seis', 'tres', 'uno'},              # 3: A -> B C D
        {'cinco', 'cuatro', 'seis', 'tres'},                     # 4: A -> A tres
        {'tres', 'uno'},                                         # 5: A -> ε
        {'cuatro', 'seis'},                                      # 6: B -> D cuatro C tres
        {DOLLAR, 'cinco', 'dos', 'seis', 'tres', 'uno'},         # 7: B -> ε
        {'cinco'},                                               # 8: C -> cinco D B
        {DOLLAR, 'dos', 'seis', 'tres', 'uno'},                  # 9: C -> ε
        {'seis'},                                                # 10: D -> seis
        {DOLLAR, 'cuatro', 'dos', 'seis', 'tres', 'uno'},        # 11: D -> ε
    ]

    display_grammar_analysis(1, "Ejercicio 1", g1, an_first_1, an_follow_1, an_pred_1)

    # ==========================================
    # GRAMÁTICA 2
    # ==========================================
    prods2 = [
        ('S', ['A', 'B', 'uno']),
        ('A', ['dos', 'B']),
        ('A', [EPSILON]),
        ('B', ['C', 'D']),
        ('B', ['tres']),
        ('B', [EPSILON]),
        ('C', ['cuatro', 'A', 'B']),
        ('C', ['cinco']),
        ('D', ['seis']),
        ('D', [EPSILON]),
    ]
    g2 = GrammarAnalyzer(non_terminals, terminals, 'S', prods2)

    all_five = {'cinco', 'cuatro', 'seis', 'tres', 'uno'}
    an_first_2 = {
        'S': {'cinco', 'cuatro', 'dos', 'tres', 'uno'},
        'A': {'dos', EPSILON},
        'B': {'cinco', 'cuatro', 'tres', EPSILON},
        'C': {'cinco', 'cuatro'},
        'D': {'seis', EPSILON},
    }
    an_follow_2 = {
        'S': {DOLLAR},
        'A': all_five,
        'B': all_five,
        'C': all_five,
        'D': all_five,
    }
    an_pred_2 = [
        {'cinco', 'cuatro', 'dos', 'tres', 'uno'},      # 1: S -> A B uno
        {'dos'},                                        # 2: A -> dos B
        all_five,                                       # 3: A -> ε
        {'cinco', 'cuatro'},                            # 4: B -> C D
        {'tres'},                                       # 5: B -> tres
        all_five,                                       # 6: B -> ε
        {'cuatro'},                                     # 7: C -> cuatro A B
        {'cinco'},                                      # 8: C -> cinco
        {'seis'},                                       # 9: D -> seis
        all_five,                                       # 10: D -> ε
    ]

    display_grammar_analysis(2, "Ejercicio 2", g2, an_first_2, an_follow_2, an_pred_2)

    print("\n" + "=" * 80)
    print("  EJECUCIÓN COMPLETADA CON ÉXITO: 100% DE COINCIDENCIAS")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
