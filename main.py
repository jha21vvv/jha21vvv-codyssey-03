import json  # 파일 저장을 위해 필요합니다.




def show_menu():
    """사용자에게 선택지를 보여주는 함수"""
    print("\n" + "="*30)
    print("   MAC 연산 시뮬레이터")
    print("="*30)
    print("1. 사용자 입력 모드 (3x3)")
    print("2. JSON 데이터 분석 모드")
    print("3. 패턴 생성기 (보너스)")
    print("4. 프로그램 종료")
    print("="*30)

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

def get_user_input():
    print("\n--- 3x3 패턴 입력 (0 또는 1) ---")
    print("예시: 0 1 0 (숫자 사이를 띄어쓰기로 구분)")
    
    user_pattern = []
    for i in range(3):
        while True:
            try:
                # 한 줄을 입력받아 공백으로 나누고 숫자로 변환합니다.
                row = list(map(int, input(f"{i+1}행 입력: ").split()))
                
                # 숫자가 정확히 3개인지 확인합니다.
                if len(row) != 3:
                    print("❌ 정확히 3개의 숫자를 입력해주세요.")
                    continue
                
                user_pattern.append(row)
                break
            except ValueError:
                print("❌ 숫자(0 또는 1)만 입력 가능합니다.")
                
    return user_pattern

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
        show_menu()
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
            print("\n[안내] JSON 데이터 분석을 시작합니다. (구현 예정)")
            # 여기에 나중에 Step 6에서 만들 함수를 넣을 거예요.
            
        elif choice == '3':
            print("\n[안내] 패턴 생성기를 실행합니다. (구현 예정)")
            # 여기에 나중에 Step 5에서 만들 함수를 넣을 거예요.
            
        elif choice == '4':
            print("\n[안내] 프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break  # while 루프를 빠져나가 프로그램을 종료합니다.
            
        else:
            print("\n[오류] 잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.")
    
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