"""
Pruebas unitarias para grammar_analyzer.py
Verifica la exactitud de PRIMEROS, SIGUIENTES y PREDICCIÓN contra los resultados analíticos.
"""

import unittest
from grammar_analyzer import GrammarAnalyzer, EPSILON, DOLLAR

class TestGrammarAnalysis(unittest.TestCase):
    def setUp(self):
        # Gramática 1
        nt1 = ['S', 'A', 'B', 'C', 'D']
        t1 = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis']
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
        self.g1 = GrammarAnalyzer(nt1, t1, 'S', prods1)

        # Gramática 2
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
        self.g2 = GrammarAnalyzer(nt1, t1, 'S', prods2)

    def test_grammar1_first(self):
        first, _ = self.g1.compute_first()
        expected = {
            'S': {'cinco', 'cuatro', 'seis', 'tres', 'uno'},
            'A': {'cinco', 'cuatro', 'seis', 'tres', EPSILON},
            'B': {'cuatro', 'seis', EPSILON},
            'C': {'cinco', EPSILON},
            'D': {'seis', EPSILON},
        }
        self.assertEqual(first, expected)

    def test_grammar1_follow(self):
        first, _ = self.g1.compute_first()
        follow, _ = self.g1.compute_follow(first)
        expected = {
            'S': {DOLLAR, 'dos'},
            'A': {'tres', 'uno'},
            'B': {DOLLAR, 'cinco', 'dos', 'seis', 'tres', 'uno'},
            'C': {DOLLAR, 'dos', 'seis', 'tres', 'uno'},
            'D': {DOLLAR, 'cuatro', 'dos', 'seis', 'tres', 'uno'},
        }
        self.assertEqual(follow, expected)

    def test_grammar1_prediction(self):
        first, _ = self.g1.compute_first()
        follow, _ = self.g1.compute_follow(first)
        preds = self.g1.compute_prediction(first, follow)
        pred_sets = [p['pred_set'] for p in preds]
        
        expected = [
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
        self.assertEqual(pred_sets, expected)

    def test_grammar1_not_ll1(self):
        first, _ = self.g1.compute_first()
        follow, _ = self.g1.compute_follow(first)
        preds = self.g1.compute_prediction(first, follow)
        is_ll1, conflicts = self.g1.check_ll1_conflicts(preds)
        self.assertFalse(is_ll1)
        self.assertTrue(len(conflicts['S']) > 0)
        self.assertTrue(len(conflicts['A']) > 0)
        self.assertTrue(len(conflicts['B']) > 0)
        self.assertTrue(len(conflicts['D']) > 0)

    def test_grammar2_first(self):
        first, _ = self.g2.compute_first()
        expected = {
            'S': {'cinco', 'cuatro', 'dos', 'tres', 'uno'},
            'A': {'dos', EPSILON},
            'B': {'cinco', 'cuatro', 'tres', EPSILON},
            'C': {'cinco', 'cuatro'},
            'D': {'seis', EPSILON},
        }
        self.assertEqual(first, expected)

    def test_grammar2_follow(self):
        first, _ = self.g2.compute_first()
        follow, _ = self.g2.compute_follow(first)
        all_five = {'cinco', 'cuatro', 'seis', 'tres', 'uno'}
        expected = {
            'S': {DOLLAR},
            'A': all_five,
            'B': all_five,
            'C': all_five,
            'D': all_five,
        }
        self.assertEqual(follow, expected)

    def test_grammar2_prediction(self):
        first, _ = self.g2.compute_first()
        follow, _ = self.g2.compute_follow(first)
        preds = self.g2.compute_prediction(first, follow)
        pred_sets = [p['pred_set'] for p in preds]

        all_five = {'cinco', 'cuatro', 'seis', 'tres', 'uno'}
        expected = [
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
        self.assertEqual(pred_sets, expected)

    def test_grammar2_not_ll1(self):
        first, _ = self.g2.compute_first()
        follow, _ = self.g2.compute_follow(first)
        preds = self.g2.compute_prediction(first, follow)
        is_ll1, conflicts = self.g2.check_ll1_conflicts(preds)
        self.assertFalse(is_ll1)
        self.assertEqual(len(conflicts['S']), 0)
        self.assertEqual(len(conflicts['A']), 0)
        self.assertEqual(len(conflicts['C']), 0)
        self.assertTrue(len(conflicts['B']) > 0)
        self.assertTrue(len(conflicts['D']) > 0)

if __name__ == '__main__':
    unittest.main()
