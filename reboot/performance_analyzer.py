import time
import random

# 간단하게 performance_analyzer.py 위부분에 임포프로 from mac_engine import MACEngine이걸 데려와도 되지?
# 나중에 구조가 복잡해져서 다음과 같은 상황이 벌어지면 프로그램이 에러를 내며 멈춥니다.
#performance_analyzer.py가 mac_engine.py를 임포트함.
#그런데 실수로 mac_engine.py도 performance_analyzer.py를 임포트함.
#결과: 서로가 서로를 기다리다가 무한 루프에 빠져 실행이 안 됨!
#지금처럼 하면 나중에 시뮬레이션에서 한줄만 바꿔주면 mac_engine.py를 다른 파일로 업그레이드도 쉽게함

class PerformanceAnalyzer:
    def __init__(self, engine):
        self.engine = engine
        # 시뮬레이레이터에 받은 엔진을 이걸로 쓰겠다고 받는다고 표시
        # 시뮬레이터에서 있던 코드: self.pa = PerformanceAnalyzer(self.engine)
        #이게 의존성 주입으로 맥의 코드를  PerformanceAnalyzer에서 self.engine을 받기로 미리 약속한셈

    def run_benchmark(self, sizes=[3, 9, 15, 25], iterations=100):
        """크기별 성능 측정 (Step 8 보너스)"""
        results = []
        for size in sizes:
            mat_a = [[random.random() for _ in range(size)] for _ in range(size)]
            mat_b = [[random.random() for _ in range(size)] for _ in range(size)]
            # random.random(): 0.0에서 1.0 사이의 랜덤한 실수 하나를 생성
            # for _ in range(size): size번만큼 반
            # 2D 측정
            start = time.time()
            #100회 반복
            for _ in range(iterations):
                self.engine.mac_2d(mat_a, mat_b)
                #그래서 여기서 엔진을 기반으로 쓸수 있는 셈.
            t2d = (time.time() - start) / iterations
            #시간이 얼마나 걸렸는지 평균으로 계산 시킴

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
        #: : "이제부터 어떻게 출력할지 형식을 지정하겠다"라는 신호입니다.
        #< : 왼쪽 정렬을 의미합니다. (화살표 방향이라고 생각하면 쉬워요! 왼쪽으로 밀어붙이기)
        #12 : 글자가 들어갈 전체 칸수입니다.
        print("-" * 60)
        for r in results:
            print(f"{r['size']:<12} | {r['t2d']*1000:<12.4f} | {r['t1d']*1000:<12.4f} | {r['impv']:<10.1f}%")
        print("="*60)