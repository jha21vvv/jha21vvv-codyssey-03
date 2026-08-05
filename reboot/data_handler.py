import json

class DataHandler:
    @staticmethod
    def get_3x3_input():
        """사용자로부터 3x3 패턴 입력 받기 (Step 4)"""
        print("\n[입력] 3x3 패턴을 입력하세요 (예: 0 1 0)")
        pattern = []
        for i in range(3):
            while True:
                try:
                    row = [int(x) for x in input(f"{i+1}행: ").split()]
                    if len(row) != 3: raise ValueError
                    pattern.append(row)
                    break
                except ValueError:
                    print("[오류] 숫자 3개를 정확히 입력해주세요.")
        return pattern

    @staticmethod
    def save_results(filename, data):
        """결과를 JSON으로 저장 (Step 6)"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"\n[알림] 결과가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"[오류] 저장 실패: {e}")

    @staticmethod
    def analyze_json_report(filename):
        """JSON 파일을 읽어 PASS/FAIL 판정 (Step 6, 7)"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"\n--- {filename} 통합 테스트 리포트 ---")
            for entry in data:
                # 실제 결과와 예상 결과 비교 로직 (단순 예시)
                status = "PASS" if entry.get('score', 0) > 3 else "FAIL"
                print(f"ID: {entry.get('timestamp', 'N/A')} | 결과: {entry['predicted']} | 상태: {status}")
        except FileNotFoundError:
            print("[오류] 분석할 파일이 없습니다.")