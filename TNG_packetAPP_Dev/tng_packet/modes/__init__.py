from .base import BaseModem

# 나중에 여기에 새로 만든 모드 파일들을 import 하세요
# from .mode_chirp import ChirpModem 

def get_available_modes():
    """
    사용 가능한 모든 모드 클래스를 리스트로 반환합니다.
    """
    modes = []
    # modes.append(ChirpModem())
    return modes
