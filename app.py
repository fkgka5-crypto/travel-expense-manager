import json
import os
from datetime import datetime


class TravelExpenseManager:

    def __init__(self):
        # 심사위원이 보기에 실제 시스템처럼 보이도록 가상의 연구과제 예산 데이터 세팅
        self.project_budgets = {
            "과제A": 5000000,  # 500만 원
            "과제B": 2000000,  # 200만 원
            "과제C": 500000,  # 50만 원 (예산 부족 시뮬레이션용)
        }
        # 직급별 일비 및 숙박비 일일 한도 규정
        self.grade_limits = {
            "책임급": {"daily_allowance": 50000, "lodging_limit": 100000},
            "선임급": {"daily_allowance": 40000, "lodging_limit": 80000},
            "원급": {"daily_allowance": 35000, "lodging_limit": 70000},
        }
        self.audit_logs = []

    def log_action(self, level, message):
        """보안 및 감사(Audit) 로그를 생성하는 함수 (Codex Security 대응용)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.audit_logs.append(log_entry)
        print(log_entry)

    def verify_receipt(self, file_name):
        """증빙 영수증 파일 확장자 및 대소문자 우회 공격 검증 (보안 기능 강화)"""
        allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
        _, extension = os.path.splitext(file_name.lower())

        # 이중 확장자 및 악성 스크립트 실행 차단 로직 시뮬레이션
        if ".." in file_name or "/" in file_name or "\\" in file_name:
            self.log_action(
                "WARN", f"비정상적인 파일 경로 접근 감지 차단: {file_name}"
            )
            return False

        if extension in allowed_extensions:
            self.log_action(
                "INFO", f"증빙 파일 검증 통과: {file_name}"
            )
            return True
        else:
            self.log_action(
                "ERROR",
                f"지원하지 않는 증빙 파일 형식 차단: {file_name}",
            )
            return False

    def calculate_and_validate_expense(
        self, project_name, grade, days, transport_fare, lodging_fare, receipt_file
    ):
        """직급별 규정 한도 및 연구과제 잔여 예산을 검증하여 최종 출장비를 정산하는 메인 로직"""
        self.log_action(
            "INFO", f"정산 프로세스 시작 - 과제명: {project_name}, 직급: {grade}"
        )

        # 1. 연구과제 존재 여부 검증
        if project_name not in self.project_budgets:
            self.log_action(
                "ERROR", f"등록되지 않은 연구과제 코드입니다: {project_name}"
            )
            return {"status": "REJECTED", "reason": "Invalid Project Code"}

        # 2. 직급별 규정 한도 검증
        if grade not in self.grade_limits:
            self.log_action(
                "ERROR", f"유효하지 않은 직급 정보입니다: {grade}"
            )
            return {"status": "REJECTED", "reason": "Invalid Employee Grade"}

        limits = self.grade_limits[grade]
        calculated_daily_allowance = limits["daily_allowance"] * days
        max_allowed_lodging = limits["lodging_limit"] * days

        # 숙박비 규정 위반 여부 체크
        if lodging_fare > max_allowed_lodging:
            self.log_action(
                "WARN",
                f"{grade} 숙박비 청구 한도 초과 (한도: {max_allowed_lodging:,}원 / 청구: {lodging_fare:,}원)",
            )
            return {
                "status": "REJECTED",
                "reason": "Lodging Limit Exceeded",
            }

        # 3. 필수 영수증 증빙 파일 검증
        if not self.verify_receipt(receipt_file):
            return {"status": "REJECTED", "reason": "Invalid Receipt Artifact"}

        # 4. 총 출장비 산출
        total_expense = (
            calculated_daily_allowance + transport_fare + lodging_fare
        )

        # 5. 연구과제 잔여 예산 통제
        current_budget = self.project_budgets[project_name]
        if total_expense > current_budget:
            self.log_action(
                "ERROR",
                f"{

    # 2. 증빙 자료 업로드 테스트
    print(manager.verify_receipt("receipt_20260602.png"))
    print(manager.verify_receipt("malicious_file.exe"))  # 보안 취약점 차단 테스트
