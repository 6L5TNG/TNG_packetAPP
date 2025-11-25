import sys
import os
import json
import subprocess
from pathlib import Path

# 설정: 실제 배포 시 GitHub 주소로 변경 필요
VERSION_FILE = "version.json"
APP_ENTRY = "tng_packet/main.py"

def check_update():
    """
    나중에 여기에 GitHub 버전 확인 로직을 넣으세요.
    지금은 단순히 현재 버전을 출력합니다.
    """
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            v = json.load(f)
            print(f"[Launcher] 현재 버전: {v.get('version', 'unknown')}")
    else:
        print("[Launcher] 버전 파일이 없습니다.")

def run_app():
    """메인 프로그램을 실행합니다."""
    print(f"[Launcher] {APP_ENTRY} 실행 중...")
    if not os.path.exists(APP_ENTRY):
        print(f"[Error] {APP_ENTRY} 파일을 찾을 수 없습니다.")
        input("아무 키나 누르면 종료합니다...")
        return

    # 파이썬으로 메인 앱 실행
    subprocess.run([sys.executable, APP_ENTRY])

if __name__ == "__main__":
    print("=== TNG Packet APP Launcher ===")
    check_update()
    print("-------------------------------")
    run_app()
