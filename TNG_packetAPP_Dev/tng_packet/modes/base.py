class BaseModem:
    """
    모든 통신 모드가 상속받아야 할 기본 클래스입니다.
    새로운 패킷을 만들 때는 이 클래스를 복사해서 쓰세요.
    """
    NAME = "Unknown"
    VERSION = "0.0"

    def __init__(self, sample_rate=48000):
        self.sr = sample_rate

    def modulate(self, text):
        """
        [송신] 텍스트를 입력받아 오디오 샘플(numpy array)을 반환해야 합니다.
        """
        raise NotImplementedError("송신 기능이 구현되지 않았습니다.")

    def demodulate(self, audio_samples):
        """
        [수신] 오디오 샘플을 받아 텍스트를 반환해야 합니다.
        """
        raise NotImplementedError("수신 기능이 구현되지 않았습니다.")
