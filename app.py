import os


class TravelExpenseManager:

    def __init__(self):
        self.expense_records = []

    def calculate_total_expense(self, daily_allowance, transport_fare, days):
        """일비와 교통비를 정산하여 총 출장비를 계산하는 함수"""
        if days <= 0:
            return 0
        total = (daily_allowance * days) + transport_fare
        return total

    def verify_receipt(self, file_name):
        """증빙 영수증 파일의 확장자를 검증하는 보안 및 관리 함수"""
        allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
        _, extension = os.path.splitext(file_name.lower())

        if extension in allowed_extensions:
            return f"[성공] {file_name} 증빙 자료가 정상적으로 등록되었습니다."
        else:
            return f"[실패] 지원하지 않는 파일 형식입니다. (올바른 확장자: JPG, PNG, PDF)"


# --- 시스템 작동 테스트 ---
if __name__ == "__main__":
    manager = TravelExpenseManager()

    print("=== 출장비 정산 및 증빙 관리 시스템 작동 ===")

    # 1. 출장비 정산 시뮬레이션 (일비 50,000원 * 3일 + KTX 교통비 60,000원)
    total = manager.calculate_total_expense(
        daily_allowance=50000, transport_fare=60000, days=3
    )
    print(f"▶ 계산된 총 출장비: {total:,}원")

    # 2. 증빙 자료 업로드 테스트
    print(manager.verify_receipt("receipt_20260602.png"))
    print(manager.verify_receipt("malicious_file.exe"))  # 보안 취약점 차단 테스트
