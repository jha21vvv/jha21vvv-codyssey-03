import json  # 파일 저장을 위해 필요합니다.
import time
import random



def display_menu():
    print("\n=== MAC 연산 시뮬레이터 (Full Version) ===")
    print("1. 수동 패턴 입력 및 판정 (3x3)")
    print("2. JSON 배치 파일 분석 (PASS/FAIL 판정)")
    print("3. 자동 패턴 생성 및 성능 비교 (3x3 ~ 25x25)")
    print("4. 종료")


# Step 4: 표준 패턴 데이터 정의 (이 내용을 함수들 위에 추가하거나 적당한 곳에 넣을 거예요)

# 3x3 표준 패턴 (2차원 리스트 형태)
PLUS_PATTERN = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]

X_PATTERN = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]
# 여러 패턴을 하나로 묶어서 관리하는 '사전(Dictionary)'입니다.
PATTERNS = {
    'CROSS': PLUS_PATTERN,
    'X': X_PATTERN
}
def generate_standard_pattern(size, p_type="cross"):
    """size x size 크기의 표준 패턴(cross 또는 x)을 생성합니다."""
    matrix = [[0] * size for _ in range(size)]
    mid = size // 2
    
    for i in range(size):
        for j in range(size):
            if p_type == "cross": # 십자가 (+)
                if i == mid or j == mid:
                    matrix[i][j] = 1
            elif p_type == "x": # 대각선 (X)
                if i == j or i + j == size - 1:
                    matrix[i][j] = 1
    return matrix

def analyze_json_file(filename="results.json"):
    """저장된 JSON 데이터를 불러와 실제 결과와 예상 결과를 비교합니다."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"\n--- {filename} 분석 리포트 ---")
        total = len(data)
        passed = 0
        
        for entry in data:
            # 여기서는 저장된 결과가 'X'인지 'Cross'인지 확인하는 로직
            # 실제 프로젝트에서는 entry['expected']와 비교하여 PASS/FAIL 결정
            print(f"ID: {entry['timestamp']} | 판정: {entry['predicted']} | 점수: {entry['score']:.2f} -> PASS")
            passed += 1
            
        print(f"\n결과: {passed}/{total} 통과 (성공률: {(passed/total)*100:.1f}%)")
    except FileNotFoundError:
        print("[오류] 분석할 JSON 파일이 없습니다.")

def print_performance_report(results):
    """테스트 결과를 표 형태로 출력"""
    print("\n" + "="*50)
    print(f"{'Size':<10} | {'2D Time(s)':<12} | {'1D Time(s)':<12} | {'Impv(%)':<8}")
    print("-" * 50)
    for res in results:
        print(f"{res['size']:<10} | {res['time_2d']:<12.4f} | {res['time_1d']:<12.4f} | {res['impv']:<8.1f}%")
    print("="*50)

def run_performance_test(size=100, iterations=1000):
    """2D MAC와 1D MAC의 실행 속도를 비교합니다."""
    print(f"\n[성능 테스트] 크기: {size}x{size}, 반복 횟수: {iterations}회")
    
    # 테스트용 랜덤 데이터 생성
    matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
    matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]
    
    # 1. 2D MAC 시간 측정
    start_time = time.time()
    for _ in range(iterations):
        # 이전에 만든 mac_2d 함수를 호출한다고 가정합니다.
        # 여기서는 간단히 로직만 표현하겠습니다.
        result_2d = 0
        for i in range(size):
            for j in range(size):
                result_2d += matrix_a[i][j] * matrix_b[i][j]
    end_time = time.time()
    time_2d = end_time - start_time
    
    # 2. 1D MAC 시간 측정 (Flatten 과정 포함)
    start_time = time.time()
    for _ in range(iterations):
        # 1차원으로 변환(Flatten)
        flat_a = [item for sublist in matrix_a for item in sublist]
        flat_b = [item for sublist in matrix_b for item in sublist]
        
        result_1d = 0
        for i in range(len(flat_a)):
            result_1d += flat_a[i] * flat_b[i]
    end_time = time.time()
    time_1d = end_time - start_time
    
    # 결과 출력
    print(f" - 2D 방식 소요 시간: {time_2d:.4f}초")
    print(f" - 1D 방식 소요 시간: {time_1d:.4f}초")
    
    if time_1d < time_2d:
        improvement = ((time_2d - time_1d) / time_2d) * 100
        print(f" >> 1D 방식이 {improvement:.1f}% 더 빠릅니다! 🚀")
    else:
        print(" >> 현재 환경에서는 2D 방식이 더 빠르거나 비슷합니다.")

def get_user_input():
    """사용자로부터 3x3 패턴을 입력받는 함수 (예외 처리 추가)"""
    print("\n3x3 패턴을 입력하세요 (0 또는 1 입력, 예: 0 1 0)")
    pattern = []
    for i in range(3):
        while True: # 올바른 입력을 할 때까지 반복
            try:
                row_input = input(f"{i+1}행 입력: ").split()
                # 숫자로 변환하고, 0 또는 1인지 확인
                row = [int(x) for x in row_input]
                
                if len(row) != 3:
                    print("[오류] 반드시 3개의 숫자를 입력해야 합니다.")
                    continue
                
                pattern.append(row)
                break # 성공하면 while문 탈출
            except ValueError:
                print("[오류] 숫자(0 또는 1)만 입력 가능합니다. 다시 입력해 주세요.")
    return pattern

def save_result_to_json(pattern, result_name, score):
    """분석 결과를 JSON 파일로 저장합니다."""
    data = {
        "user_pattern": pattern,
        "detected_pattern": result_name,
        "similarity_score": score
    }
    
    with open("analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("\n[시스템] 분석 결과가 'analysis_result.json'에 저장되었습니다!")

def main():
    """프로그램의 전체 흐름을 제어하는 메인 함수"""
    while True:
        display_menu()
        choice = input("원하는 메뉴 번호를 입력하세요: ")
        if choice == '1':
            # [Step 5] 사용자로부터 3x3 패턴 직접 입력받기
            user_pattern = get_user_input()
            
            print("\n--- 입력하신 패턴 확인 ---")
            for row in user_pattern:
                print(row)
            # --- Step 6: MAC 연산을 통한 패턴 판정 ---
            print("\n--- 분석 결과 ---")
            
            best_match = ""
            highest_score = -1.0
            
            # PATTERNS 딕셔너리에 저장된 모든 패턴과 비교합니다.
            for name, standard_pattern in PATTERNS.items():
                # Step 2에서 만든 mac_2d 함수 사용!
                score = mac_2d(user_pattern, standard_pattern)
                print(f"[{name}] 패턴과의 유사도 점수: {score}")
                
                # 가장 높은 점수를 받은 패턴을 기억합니다.
                if score > highest_score:
                    highest_score = score
                    best_match = name
            
            # 최종 결과 출력
            if highest_score > 0:
                print(f"결과: 이 패턴은 '{best_match}'일 확률이 가장 높습니다!")
                print(f"최종 점수: {highest_score}")
                
                # --- Step 7: 결과 저장 호출 ---
                save_result_to_json(user_pattern, best_match, highest_score)
            else:
                print("결과: 일치하는 패턴을 찾을 수 없습니다.")    
        elif choice == '2':
            analyze_json_file() # Step 6, 7
        elif choice == '3':
            # Step 8, 9: 반복문을 돌며 다양한 크기 테스트 후 리포트 출력
            performance_results = []
            for s in [3, 9, 15, 25]:
                # 여기서 테스트 실행 후 performance_results에 append
                pass
            print_performance_report(performance_results)
        elif choice == '4':
            break

        else:
            print("\n[오류] 잘못된 선택입니다. 1번~3번을 입력해 주세요.")
    
def mac_2d(matrix_a, matrix_b):
    """
    2차원 리스트를 입력받아 MAC 연산을 수행 (기본 방식)
    결과 = sum(matrix_a[i][j] * matrix_b[i][j])
    """
    result = 0.0
    size = len(matrix_a) # 행의 개수 (N)
    
    for i in range(size):
        for j in range(size):
            result += matrix_a[i][j] * matrix_b[i][j]
            
    return result

def mac_1d(flat_a, flat_b):
    """
    1차원 리스트를 입력받아 MAC 연산을 수행 (최적화 방식)
    """
    result = 0.0
    # zip을 사용하면 두 리스트의 요소를 하나씩 짝지어 가져옵니다.
    for val_a, val_b in zip(flat_a, flat_b):
        result += val_a * val_b
        
    return result

def flatten(matrix):
    """2차원 리스트를 1차원으로 변환하는 도우미 함수"""
    return [item for sublist in matrix for item in sublist]

def normalize_label(label):
    """
    사용자가 입력한 다양한 라벨을 표준 형식으로 변환합니다.
    - '+', 'cross', 'plus' -> 'CROSS'
    - 'x', 'X', 'multiply' -> 'X'
    """
    # 공백 제거 및 소문자 변환으로 오타 방지
    label = label.strip().lower()
    
    cross_aliases = ['+', 'cross', 'plus']
    x_aliases = ['x', 'X', 'multiply'] # 'X'는 이미 소문자 'x'로 변환됨
    
    if label in cross_aliases:
        return "CROSS"
    elif label in x_aliases:
        return "X"
    else:
        return None # 알 수 없는 입력일 경우

# 이 파일이 직접 실행될 때만 main() 함수를 호출합니다.
if __name__ == "__main__":
    main()