import os
import math
import struct
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._init_sounds()
        except Exception as e:
            print(f"Аудіо недоступне: {e}")
            self.enabled = False

    def _generate_tone(self, freq_start, freq_end, duration, volume=0.5, is_noise=False):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / float(sample_rate)
            if is_noise:
                import random
                val = int(random.uniform(-1, 1) * 32767 * volume * (1.0 - t/duration))
            else:
                freq = freq_start + (freq_end - freq_start) * (t / duration)
                val = int(math.sin(2 * math.pi * freq * t) * 32767 * volume * (1.0 - t/duration))
            val = max(-32768, min(32767, val))
            # 2 канали (стерео)
            packed = struct.pack("<hh", val, val)
            buf.extend(packed)
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _init_sounds(self):
        # Клік
        self.sounds["click"] = self._generate_tone(350, 150, 0.08, volume=0.3)
        # Покупка
        self.sounds["buy"] = self._generate_tone(520, 880, 0.12, volume=0.25)
        # Хорор-скример (потужний низькочастотний дісторшн і шум)
        horror_file = "assets/sounds/horror_scream.wav"
        if os.path.exists(horror_file):
            try:
                self.sounds["horror"] = pygame.mixer.Sound(horror_file)
            except Exception:
                self.sounds["horror"] = self._generate_tone(120, 40, 1.2, volume=0.85, is_noise=True)
        else:
            self.sounds["horror"] = self._generate_tone(120, 40, 1.2, volume=0.85, is_noise=True)

    def play(self, name):
        if self.enabled and name in self.sounds:
            try:
                self.sounds[name].play()
            except Exception:
                pass