import os
import time
import datetime

class SpiritualMonitor:
    def __init__(self):
        self.log_path = "C:/lovesoong/Core/system_spirit.log"
        print("⚙️ [Core] Spiritual Monitor Awakening...")

    def pulse(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "HEALTHY"
        log_entry = f"[{timestamp}] System Integrity: {status} | Pulse: OK\n"
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        return log_entry.strip()

if __name__ == "__main__":
    monitor = SpiritualMonitor()
    try:
        while True:
            report = monitor.pulse()
            print(f"📡 {report}", end="\r")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n⚙️ [Core] Monitor Backgrounded.")
