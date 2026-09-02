import datetime
from datetime import timedelta

class VaccineScheduler:
    """
    육아 아빠를 위한 자동 예방접종 일정 계산 및 ICS 캘린더 파일 생성기
    """
    def __init__(self, child_name: str, birth_date_str: str):
        self.child_name = child_name
        self.birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        self.schedule = []

    def add_vaccine(self, name: str, offset_months: int):
        # 개월 수 기반 대략적인 접종 예정일 계산 (1개월 = 30일 기준)
        target_date = self.birth_date + timedelta(days=offset_months * 30)
        self.schedule.append({"vaccine": name, "date": target_date})

    def generate_ics(self, output_filename="vaccine_schedule.ics"):
        """iCalendar(.ics) 파일 표준 포맷으로 내보내기"""
        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Childcare Auto Scheduler//KR"
        ]
        
        for item in self.schedule:
            event_date = item["date"].strftime("%Y%m%d")
            summary = f"[{self.child_name}] {item['vaccine']} 예방접종 예정일"
            
            ics_content.extend([
                "BEGIN:VEVENT",
                f"SUMMARY:{summary}",
                f"DTSTART;VALUE=DATE:{event_date}",
                f"DESCRIPTION:{self.child_name}의 {item['vaccine']} 접종 권장일입니다. 병원 예약을 확인하세요.",
                "END:VEVENT"
            ])
            
        ics_content.append("END:VCALENDAR")
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(ics_content))
            
        print(f"✅ {output_filename} 생성 완료! 구글/아이폰 캘린더에 가져오기(Import)하세요.")

if __name__ == "__main__":
    # 예시 사용법
    print("👶 육아 맞춤 예방접종 캘린더 생성기")
    baby_name = "단우"
    birth = "2024-01-15"
    
    scheduler = VaccineScheduler(child_name=baby_name, birth_date_str=birth)
    
    # 주요 필수 예방접종 일정 등록 (개월 수 기준)
    scheduler.add_vaccine("B형간염 1차", 0)
    scheduler.add_vaccine("B형간염 2차", 1)
    scheduler.add_vaccine("DTaP / 폴리오 1차", 2)
    scheduler.add_vaccine("DTaP / 폴리오 2차", 4)
    scheduler.add_vaccine("DTaP / 폴리오 3차", 6)
    scheduler.add_vaccine("MMR / 수두 1차", 12)
    
    scheduler.generate_ics()

