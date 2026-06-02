import json
import os
from datetime import datetime


class TravelExpenseManager:

    def __init__(self):
        # [시스템 초기화] 연구과제 마스터 데이터 및 가용 예산 계정 정의
        self.project_budgets = {
            "과제A": 5000000,  # 국책연구과제 A비용 잔액
            "과제B": 2000000,  # 민간수탁과제 B비용 잔액
            "과제C": 500000,  # 기관고유과제 C비용 잔액
        }

        # [여비 정산 기준] 기관 내부 규정에 따른 직급별 일비 및 숙박비 수행 한도
        self.grade_limits = {
            "책임급": {"daily_allowance": 50000, "lodging_limit": 100000},
            "선임급": {"daily_allowance": 40000, "lodging_limit": 80000},
            "원급": {"daily_allowance": 35000, "lodging_limit": 70000},
        }
        self.audit_logs = []

    def log_action(self, level, message):
        """보안 및 감사(Audit) 로그 생성 시스템 (Codex Security 연동 표준)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.audit_logs.append(log_entry)
        print(log_entry)

    def verify_receipt(self, file_name):
        """증빙 파일 무결성 및 확장자 보안 검증 로직"""
        allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
        _, extension = os.path.splitext(file_name.lower())

        # 디렉토리 트래버스(경로 우회) 및 파일 시스템 위협 방지 로직
        if ".." in file_name or "/" in file_name or "\\" in file_name:
            self.log_action(
                "WARN", f"비정상적인 파일 경로 접근 유효성 검증 실패: {file_name}"
            )
            return False

        if extension in allowed_extensions:
            self.log_action(
                "INFO", f"증빙 파일 포맷 검증 완료: {file_name}"
            )
            return True
        else:
            self.log_action(
                "ERROR",
                f"미승인 증빙 확장자 차단 (허용: JPG, PNG, PDF): {file_name}",
            )
            return False

    def calculate_and_validate_expense(
        self, project_name, grade, days, transport_fare, lodging_fare, receipt_file
    ):
        """연구과제 예산 통제 및 여비 규정 한도 검증 기반의 최종 정산 메인 통제 로직"""
        self.log_action(
            "INFO",
            f"여비 정산 프로세스 개시 - 과제코드: {project_name}, 신청직급: {grade}",
        )

        # 1. 과제 코드 유효성 검증
        if project_name not in self.project_budgets:
            self.log_action(
                "ERROR", f"미등록 연구과제 코드 접근 차단: {project_name}"
            )
            return {"status": "REJECTED", "reason": "Invalid Project Code"}

        # 2. 직급 권한 및 여비 기준 매핑 검증
        if grade not in self.grade_limits:
            self.log_action(
                "ERROR", f"유효하지 않은 직급 프로필 접근: {grade}"
            )
            return {"status": "REJECTED", "reason": "Invalid Employee Grade"}

        limits = self.grade_limits[grade]
        calculated_daily_allowance = limits["daily_allowance"] * days
        max_allowed_lodging = limits["lodging_limit"] * days

        # 숙박비 한도 초과 규정 검증
        if lodging_fare > max_allowed_lodging:
            self.log_action(
                "WARN",
                f"내부 여비 규정 위반 - {grade} 숙박비 한도 초과 (지정 한도: {max_allowed_lodging:,}원 / 신청 금액: {lodging_fare:,}원)",
            )
            return {
                "status": "REJECTED",
                "reason": "Lodging Limit Exceeded",
            }

        # 3. 필수 행정 증빙자료 검증 (Codex Security 연동 영역)
        if not self.verify_receipt(receipt_file):
            return {"status": "REJECTED", "reason": "Invalid Receipt Artifact"}

        # 4. 정산 총액 산출
        total_expense = (
            calculated_daily_allowance + transport_fare + lodging_fare
        )

        # 5. 연구과제비 잔여 예산 통제 및 한도 검증
        current_budget = self.project_budgets[project_name]
        if total_expense > current_budget:
            self.log_action(
                "ERROR",
                f"예산 통제 실패 - {project_name} 과제 예산 부족 (현재 잔액: {current_budget:,}원 / 정산 요청액: {total_expense:,}원)",
            )
            return {"status": "REJECTED", "reason": "Budget Insufficient"}

        # 6. 예산 승인 및 원장 반영
        self.project_budgets[project_name] -= total_expense
        self.log_action(
            "INFO",
            f"정산 최종 승인 완료 - 정산액: {total_expense:,}원 (과제 잔여 예산: {self.project_budgets[project_name]:,}원)",
        )

        return {
            "status": "APPROVED",
            "total_expense": total_expense,
            "remaining_budget": self.project_budgets[project_name],
        }


# --- 시스템 통합 테스트 및 유닛 시뮬레이션 ---
if __name__ == "__main__":
    manager = TravelExpenseManager()

    print("\n=== [CASE 1] 정상 정산 승인 프로세스 테스트 ===")
    result1 = manager.calculate_and_validate_expense(
        project_name="과제A",
        grade="책임급",
        days=2,
        transport_fare=65000,
        lodging_fare=180000,
        receipt_file="KTX_and_Hotel_Receipt.pdf",
    )
    print(f"결과: {json.dumps(result1, ensure_ascii=False, indent=2)}\n")

    print("=== [CASE 2] 내부 여비 규정 위반(한도 초과) 통제 테스트 ===")
    result2 = manager.calculate_and_validate_expense(
        project_name="과제B",
        grade="선임급",
        days=1,
        transport_fare=45000,
        lodging_fare=120000,
        receipt_file="receipt_image.png",
    )
    print(f"결과: {json.dumps(result2, ensure_ascii=False, indent=2)}\n")

    print("=== [CASE 3] 비정상 파일 구조 유효성 검증(보안 기능) 테스트 ===")
    result3 = manager.calculate_and_validate_expense(
        project_name="과제A",
        grade="원급",
        days=1,
        transport_fare=30000,
        lodging_fare=50000,
        receipt_file="../../malicious_script.exe",
    )
    print(f"결과: {json.dumps(result3, ensure_ascii=False, indent=2)}\n")

    print("=== [CASE 4] 과제 가용 예산 한도 초과 통제 테스트 ===")
    result4 = manager.calculate_and_validate_expense(
        project_name="과제C",
        grade="책임급",
        days=5,
        transport_fare=200000,
        lodging_fare=450000,
        receipt_file="valid_receipt.jpg",
    )
    print(f"결과: {json.dumps(result4, ensure_ascii=False, indent=2)}\n")
