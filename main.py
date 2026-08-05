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

def main():
    """프로그램의 전체 흐름을 제어하는 메인 함수"""
    while True:
        show_menu()
        choice = get_user_input("원하는 메뉴 번호를 입력하세요: ")
        if choice == '1':
            user_input = input("패턴 이름을 입력하세요 (+, cross, x, X 등): ")
            normalized = normalize_label(user_input)
            
            if normalized:
                print(f"✅ 정규화 성공: '{user_input}' -> '{normalized}'")
            else:
                print(f"❌ 알 수 없는 패턴입니다: '{user_input}'")
            
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