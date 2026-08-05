from mac_engine import MACEngine
from pattern_manager import PatternManager
from data_handler import DataHandler
from performance_analyzer import PerformanceAnalyzer
import datetime

class MACSimulator:
    def __init__(self):
        self.engine = MACEngine()
        self.pm = PatternManager()
        self.dh = DataHandler()
        self.pa = PerformanceAnalyzer(self.engine)
        self.history = []

    def run(self):
        while True:
            print("\n=== MAC 시뮬레이터 로드맵 완성판 ===")
            print("1. 수동 패턴 입력 및 판정")
            print("2. JSON 배치 파일 분석")
            print("3. 성능 분석 테스트 (3x3~25x25)")
            print("4. 종료")
            
            choice = input("메뉴 선택: ")
            if choice == '1': self.mode_manual()
            elif choice == '2': self.dh.analyze_json_report("results.json")
            elif choice == '3': self.mode_performance()
            elif choice == '4': break

    def mode_manual(self):
        user_p = self.dh.get_3x3_input()
        best_name, max_score = "", -1.0
        
        for name, std_p in self.pm.base_patterns.items():
            score = self.engine.mac_2d(user_p, std_p)
            if score > max_score:
                max_score = score
                best_name = name
        
        print(f"\n[결과] 판정: {best_name} | 유사도: {self.engine.calculate_similarity(max_score):.1f}%")
        
        # 결과 저장용 데이터 축적
        res_data = {
            "timestamp": str(datetime.datetime.now()),
            "predicted": best_name,
            "score": max_score
        }
        self.history.append(res_data)
        self.dh.save_results("results.json", self.history)

    def mode_performance(self):
        print("\n성능 테스트 중... 잠시만 기다려주세요.")
        results = self.pa.run_benchmark()
        self.pa.print_table(results)