import time
import random

class PerformanceAnalyzer:
    def __init__(self, engine):
        self.engine = engine

    def run_benchmark(self, sizes=[3, 9, 15, 25], iterations=100):
        """크기별 성능 측정 (Step 8 보너스)"""
        results = []
        for size in sizes:
            mat_a = [[random.random() for _ in range(size)] for _ in range(size)]
            mat_b = [[random.random() for _ in range(size)] for _ in range(size)]
            
            # 2D 측정
            start = time.time()
            for _ in range(iterations):
                self.engine.mac_2d(mat_a, mat_b)
            t2d = (time.time() - start) / iterations

            # 1D 측정 (변환 시간 포함)
            start = time.time()
            for _ in range(iterations):
                fa = self.engine.flatten(mat_a)
                fb = self.engine.flatten(mat_b)
                self.engine.mac_1d(fa, fb)
            t1d = (time.time() - start) / iterations

            impv = ((t2d - t1d) / t2d) * 100 if t2d > 0 else 0
            results.append({'size': size**2, 't2d': t2d, 't1d': t1d, 'impv': impv})
        return results

    def print_table(self, results):
        """성능 리포트 표 출력 (Step 9)"""
        print("\n" + "="*60)
        print(f"{'Size(N^2)':<12} | {'2D Avg(ms)':<12} | {'1D Avg(ms)':<12} | {'Improve(%)':<10}")
        print("-" * 60)
        for r in results:
            print(f"{r['size']:<12} | {r['t2d']*1000:<12.4f} | {r['t1d']*1000:<12.4f} | {r['impv']:<10.1f}%")
        print("="*60)