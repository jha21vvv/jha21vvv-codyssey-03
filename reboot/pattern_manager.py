class PatternManager:
    def __init__(self):
        # 기본 3x3 패턴 (Step 4)
        self.base_patterns = {
            'CROSS': [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
            'X': [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
        }

    def generate_dynamic_pattern(self, size, p_type="cross"):
        """N 크기에 맞는 패턴 자동 생성 (Step 5 보너스)"""
        matrix = [[0] * size for _ in range(size)]
        mid = size // 2
        for i in range(size):
            for j in range(size):
                if p_type == "cross":
                    if i == mid or j == mid: matrix[i][j] = 1
                elif p_type == "x":
                    if i == j or i + j == size - 1: matrix[i][j] = 1
        return matrix

    def normalize_label(self, label):
        """라벨 정규화 (Step 3)"""
        label = label.strip().lower()
        if label in ['+', 'cross', 'plus']: return "CROSS"
        if label in ['x', 'multiply']: return "X"
        return label.upper()