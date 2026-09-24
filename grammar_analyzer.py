"""
Módulo: grammar_analyzer.py
Implementación de algoritmos para Análisis Sintáctico Descendente:
- Cálculo de Símbolos Anulables
- Conjunto PRIMEROS (FIRST) para símbolos y cadenas
- Algoritmo de punto fijo para PRIMEROS de no terminales
- Algoritmo de punto fijo para SIGUIENTES (FOLLOW) de no terminales
- Conjunto de PREDICCIÓN (PREDICT) para cada regla de producción
- Verificación del Criterio LL(1) y construcción de la Tabla de Análisis Predictivo M[A, a]
"""

from typing import List, Set, Dict, Tuple, Optional
import sys

EPSILON = 'ε'
DOLLAR = '$'

class Production:
    """Representa una regla de producción A -> alpha."""
    def __init__(self, index: int, lhs: str, rhs: List[str]):
        self.index = index
        self.lhs = lhs
        self.rhs = rhs

    def is_epsilon_production(self) -> bool:
        return self.rhs == [EPSILON] or len(self.rhs) == 0

    def __repr__(self) -> str:
        rhs_str = " ".join(self.rhs) if self.rhs else EPSILON
        return f"{self.index}. {self.lhs} -> {rhs_str}"


class GrammarAnalyzer:
    """Analizador de Gramáticas Libres de Contexto (CFG)."""
    def __init__(self, non_terminals: List[str], terminals: List[str], 
                 start_symbol: str, productions_tuples: List[Tuple[str, List[str]]]):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        
        self.productions: List[Production] = []
        for idx, (lhs, rhs) in enumerate(productions_tuples, 1):
            cleaned_rhs = [EPSILON] if not rhs else rhs
            self.productions.append(Production(idx, lhs, cleaned_rhs))

    def first_of_sequence(self, sequence: List[str], first_sets: Dict[str, Set[str]]) -> Set[str]:
        """
        Calcula PRIMEROS(X1 X2 ... Xk) según la regla:
        PRIMEROS(X1...Xk) = U_{i=1}^k (PRIMEROS(Xi) - {ε}) hasta el primer Xi no anulable.
        Si todos son anulables (o secuencia vacía), agrega ε.
        """
        if not sequence or sequence == [EPSILON]:
            return {EPSILON}
        
        result: Set[str] = set()
        all_nullable = True
        
        for symbol in sequence:
            if symbol == EPSILON:
                continue
            elif symbol in self.terminals:
                result.add(symbol)
                all_nullable = False
                break
            elif symbol in self.non_terminals:
                sym_first = first_sets.get(symbol, set())
                result.update(sym_first - {EPSILON})
                if EPSILON not in sym_first:
                    all_nullable = False
                    break
            else:
                # Símbolo no registrado tratado como terminal
                result.add(symbol)
                all_nullable = False
                break
                
        if all_nullable:
            result.add(EPSILON)
            
        return result

    def compute_first(self, track_iterations: bool = False) -> Tuple[Dict[str, Set[str]], List[Dict[str, Set[str]]]]:
        """
        Algoritmo de punto fijo para calcular PRIMEROS(A) para cada no terminal.
        1. Inicializar PRIMEROS(A) = vacio para cada no terminal A.
        2. Recorrer todas las producciones A -> X1 ... Xk.
        3. Propagar terminales de izquierda a derecha respetando anulabilidad.
        4. Repetir hasta alcanzar un punto fijo.
        """
        first: Dict[str, Set[str]] = {nt: set() for nt in self.non_terminals}
        history: List[Dict[str, Set[str]]] = []
        
        changed = True
        iteration = 0
        while changed:
            iteration += 1
            changed = False
            for prod in self.productions:
                rhs_first = self.first_of_sequence(prod.rhs, first)
                if not rhs_first.issubset(first[prod.lhs]):
                    first[prod.lhs].update(rhs_first)
                    changed = True
            if track_iterations:
                history.append({nt: set(first[nt]) for nt in self.non_terminals})
                
        return first, history

    def compute_follow(self, first_sets: Dict[str, Set[str]], track_iterations: bool = False) -> Tuple[Dict[str, Set[str]], List[Dict[str, Set[str]]]]:
        """
        Algoritmo de punto fijo para SIGUIENTES(A).
        1. Inicializar $ in SIGUIENTES(S).
        2. Para cada produccion A -> alpha B beta:
           - Agregar PRIMEROS(beta) - {ε} a SIGUIENTES(B).
           - Si beta =>* ε o beta es vacia, agregar SIGUIENTES(A) a SIGUIENTES(B).
        3. Repetir hasta alcanzar punto fijo.
        Nota: ε nunca pertenece a un conjunto SIGUIENTES.
        """
        follow: Dict[str, Set[str]] = {nt: set() for nt in self.non_terminals}
        follow[self.start_symbol].add(DOLLAR)
        history: List[Dict[str, Set[str]]] = []
        
        changed = True
        while changed:
            changed = False
            for prod in self.productions:
                lhs = prod.lhs
                rhs = prod.rhs
                for i, symbol in enumerate(rhs):
                    if symbol in self.non_terminals:
                        beta = rhs[i+1:]
                        beta_first = self.first_of_sequence(beta, first_sets)
                        
                        # 1. Agregar PRIMEROS(beta) - {ε}
                        to_add = beta_first - {EPSILON}
                        if not to_add.issubset(follow[symbol]):
                            follow[symbol].update(to_add)
                            changed = True
                            
                        # 2. Si beta es anulable, agregar SIGUIENTES(lhs)
                        if EPSILON in beta_first:
                            if not follow[lhs].issubset(follow[symbol]):
                                follow[symbol].update(follow[lhs])
                                changed = True
            if track_iterations:
                history.append({nt: set(follow[nt]) for nt in self.non_terminals})
                
        return follow, history

    def compute_prediction(self, first_sets: Dict[str, Set[str]], 
                           follow_sets: Dict[str, Set[str]]) -> List[Dict]:
        """
        Calcula el conjunto de PREDICCIÓN de cada producción A -> alpha:
        PRED(A -> alpha) =
           PRIMEROS(alpha)                             si ε no in PRIMEROS(alpha)
           (PRIMEROS(alpha) - {ε}) U SIGUIENTES(A)     si ε in PRIMEROS(alpha)
        """
        predictions = []
        for prod in self.productions:
            alpha_first = self.first_of_sequence(prod.rhs, first_sets)
            is_nullable = EPSILON in alpha_first
            if not is_nullable:
                pred_set = set(alpha_first)
            else:
                pred_set = (alpha_first - {EPSILON}) | follow_sets[prod.lhs]
                
            predictions.append({
                'production': prod,
                'first_alpha': alpha_first,
                'is_nullable': is_nullable,
                'pred_set': pred_set
            })
        return predictions

    def check_ll1_conflicts(self, predictions: List[Dict]) -> Tuple[bool, Dict[str, List[Tuple[Production, Production, Set[str]]]]]:
        """
        Verifica el criterio LL(1):
        Para cada no terminal, los conjuntos de predicción de sus alternativas deben ser disjuntos.
        """
        conflicts: Dict[str, List[Tuple[Production, Production, Set[str]]]] = {nt: [] for nt in self.non_terminals}
        is_ll1 = True
        
        # Agrupar predicciones por no terminal
        by_nt: Dict[str, List[Dict]] = {nt: [] for nt in self.non_terminals}
        for item in predictions:
            by_nt[item['production'].lhs].append(item)
            
        for nt, items in by_nt.items():
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    intersection = items[i]['pred_set'] & items[j]['pred_set']
                    if intersection:
                        is_ll1 = False
                        conflicts[nt].append((items[i]['production'], items[j]['production'], intersection))
                        
        return is_ll1, conflicts

    def build_parsing_table(self, predictions: List[Dict]) -> Dict[str, Dict[str, List[Production]]]:
        """
        Construye la tabla predictiva LL(1) M[A, a].
        Columnas: Terminales + {$}
        Filas: No terminales
        """
        terminals_with_dollar = self.terminals + [DOLLAR]
        table: Dict[str, Dict[str, List[Production]]] = {
            nt: {t: [] for t in terminals_with_dollar} for nt in self.non_terminals
        }
        
        for item in predictions:
            prod = item['production']
            for terminal in item['pred_set']:
                if terminal in table[prod.lhs]:
                    table[prod.lhs][terminal].append(prod)
                    
        return table
