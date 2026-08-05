import json

class DataHandler:

    @staticmethod
    def normalize_label(raw_label):
        label = str(raw_label).strip().lower()
        if label in ["+", "cross", "plus"]:
            return "CROSS"
        if label in ["x"]:
            return "X"
        return "UNKNOWN"

    @staticmethod
    def load_data(filepath="data.json"):
        """data.json을 읽어서 딕셔너리로 반환"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[오류] 파일을 찾을 수 없습니다: {filepath}")
            raise
        except json.JSONDecodeError as e:
            print(f"[오류] JSON 형식이 잘못됐습니다: {e}")
            raise

    @staticmethod
    def validate_keys(data):
        """필수 키 존재 확인"""
        for key in ["filters", "patterns"]:
            if key not in data:
                raise KeyError(f"필수 키 '{key}'가 없습니다!")
        print("✔ 필수 키 확인 완료")


    @staticmethod
    def extract_size(name):
        parts = name.split("_")

        if len(parts) < 2 or parts[0] != "size":
            raise ValueError(f"잘못된 이름 형식: {name}")

        try:
            return int(parts[1])
        except ValueError:
            raise ValueError(f"크기 추출 실패: {name}")
        
    @staticmethod
    def validate_matching(data):
        """필터와 패턴의 크기가 맞는지 검증"""
        filters = data["filters"]
        patterns = data["patterns"]

        for pkey, pvalue in patterns.items():
            try:
                size = DataHandler.extract_size(pkey)   # 예: size_3_1 -> 3
                fkey = f"size_{size}"                   # 예: size_3

                if fkey not in filters:
                    raise ValueError(f"'{pkey}'에 맞는 필터 '{fkey}'가 없습니다.")

                if "input" not in pvalue:
                    raise KeyError(f"'{pkey}'에 'input' 키가 없습니다.")

                pattern_size = len(pvalue["input"])
                filter_size = DataHandler.extract_size(fkey)

                if pattern_size != filter_size:
                    raise ValueError(
                        f"크기 불일치: 패턴={pattern_size}, 기대={filter_size}"
                    )

            except (KeyError, ValueError) as e:
                print(f"[{pkey}] FAIL - {e}")

        print("✔ 필터-패턴 매칭 완료")

    @staticmethod
    def load_and_validate(filepath="data.json"):
        """로드 + 검증 통합 실행"""
        data = DataHandler.load_data(filepath)
        DataHandler.validate_keys(data)
        DataHandler.validate_matching(data)
        print(f"✔ 로드 완료! 필터 {len(data['filters'])}종, 패턴 {len(data['patterns'])}개")
        return data["filters"], data["patterns"]

    @staticmethod
    def get_3x3_input():
        """사용자로부터 3x3 패턴 입력 받기"""
        print("\n[입력] 3x3 패턴을 입력하세요 (예: 0 1 0)")
        pattern = []
        for i in range(3):
            while True:
                try:
                    row = [int(x) for x in input(f"{i+1}행: ").split()]
                    if len(row) != 3:
                        raise ValueError
                    pattern.append(row)
                    break
                except ValueError:
                    print("[오류] 숫자 3개를 정확히 입력해주세요.")
        return pattern

    @staticmethod
    def save_results(filename, data):
        """결과를 JSON으로 저장"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"\n[알림] 결과가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"[오류] 저장 실패: {e}")

    @staticmethod
    def analyze_json_report(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n--- {filename} 통합 테스트 리포트 ---")
        for entry in data:
            predicted = DataHandler.normalize_label(entry['predicted'])
            expected = DataHandler.normalize_label(entry['expected'])
            status = "PASS" if predicted == expected else "FAIL"
            print(f"예측: {predicted} | 정답: {expected} | 상태: {status}")

