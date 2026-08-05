class MACEngine:
    @staticmethod
    def mac_2d(matrix_a, matrix_b):
        """2차원 리스트 중첩 반복문 연산 (Step 2)"""
        result = 0.0
        size = len(matrix_a)
        for i in range(size):
            for j in range(size):
                result += matrix_a[i][j] * matrix_b[i][j]
        return result

    @staticmethod
    def mac_1d(flat_a, flat_b):
        """1차원 리스트 최적화 연산 (Step 2 보너스)"""
        return sum(a * b for a, b in zip(flat_a, flat_b))

    @staticmethod
    def flatten(matrix):
        """2차원을 1차원으로 변환 (Step 2 힌트)"""
        return [item for sublist in matrix for item in sublist]

    @staticmethod
    def calculate_similarity(score, max_score=5.0):
        """점수를 기반으로 유사도 백분율 계산 (Step 3)"""
        if max_score == 0: return 0
        return (score / max_score) * 100