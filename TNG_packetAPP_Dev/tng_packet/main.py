import sys
import os
import json
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.i18n import I18n
from modes import get_available_modes

def main():
    print("\n[System] TNG Packet APP 플랫폼을 시작합니다.")
    
    # 1. 언어 설정 로드
    i18n = I18n("ko") # 기본값 한국어
    print(f"[Info] 언어 설정: {i18n.get('app_title')}")
    
    # 2. 사용 가능한 모드 검색
    modes = get_available_modes()
    print(f"[Info] 감지된 통신 모듈: {len(modes)}개")
    for m in modes:
        print(f" - {m.NAME} ({m.VERSION})")
    
    print("\n[GUI] 메인 윈도우를 실행합니다... (지금은 텍스트 모드)")
    print("-----------------------------------------------------")
    print("명령을 입력하세요 (tx: 송신 테스트, exit: 종료)")
    
    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "exit":
            break
        elif cmd == "tx":
            print("어떤 모드로 송신하시겠습니까?")
            # 나중에 여기에 모드 선택 로직 추가
        else:
            print("알 수 없는 명령입니다.")

if __name__ == "__main__":
    main()
