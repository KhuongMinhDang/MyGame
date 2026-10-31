import json
import os


class RecordManager:
    """Quản lý lưu trữ và truy xuất kỷ lục thời gian tiêu diệt Boss theo từng loại Boss và Máy bay."""

    FILE_PATH = os.path.join("data", "records.json")
    NUM_BOSSES = 3
    NUM_SHIPS = 4

    def __init__(self, file_path=None):
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = self.FILE_PATH
        self.records = self._load_records()

    def _default_records(self):
        """Tạo cấu trúc mặc định: 3 Boss (0, 1, 2) và 4 Máy bay (0, 1, 2, 3)."""
        data = {}
        for b in range(self.NUM_BOSSES):
            data[str(b)] = {}
            for s in range(self.NUM_SHIPS):
                data[str(b)][str(s)] = None
        return data

    def _load_records(self):
        """Đọc file json lưu kỷ lục. Nếu chưa có hoặc lỗi thì tạo mới."""
        defaults = self._default_records()
        if not os.path.exists(self.file_path):
            return defaults

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Đảm bảo đầy đủ các key
                for b in range(self.NUM_BOSSES):
                    b_str = str(b)
                    if b_str not in data or not isinstance(data[b_str], dict):
                        data[b_str] = {}
                    for s in range(self.NUM_SHIPS):
                        s_str = str(s)
                        if s_str not in data[b_str]:
                            data[b_str][s_str] = None
                return data
        except Exception as e:
            print(f"[RecordManager] Lỗi đọc records.json: {e}, dùng mặc định.")
            return defaults

    def _save_records(self):
        """Lưu kỷ lục vào file JSON."""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[RecordManager] Lỗi ghi records.json: {e}")

    def get_record(self, boss_id: int, ship_id: int) -> float | None:
        """Lấy kỷ lục hiện tại (tính bằng giây). Trả về None nếu chưa có."""
        b_str, s_str = str(boss_id), str(ship_id)
        if b_str in self.records and s_str in self.records[b_str]:
            return self.records[b_str][s_str]
        return None

    def save_record_if_best(self, boss_id: int, ship_id: int, elapsed_sec: float) -> tuple[bool, float | None]:
        """
        Kiểm tra và cập nhật kỷ lục mới nếu thời gian ngắn hơn kỷ lục cũ (hoặc lần đầu).
        Trả về (is_new_record, old_record).
        """
        b_str, s_str = str(boss_id), str(ship_id)
        old_record = self.get_record(boss_id, ship_id)
        elapsed_sec = round(float(elapsed_sec), 2)

        if old_record is None or elapsed_sec < old_record:
            if b_str not in self.records:
                self.records[b_str] = {}
            self.records[b_str][s_str] = elapsed_sec
            self._save_records()
            return True, old_record

        return False, old_record

    def get_all_records(self) -> dict:
        """Lấy toàn bộ dữ liệu kỷ lục."""
        return self.records

    @staticmethod
    def format_time(seconds: float | None) -> str:
        """Định dạng số giây thành chuỗi MM:SS.ms (ví dụ 75.42 -> 01:15.42)."""
        if seconds is None:
            return "--:--.--"
        total_seconds = max(0.0, float(seconds))
        minutes = int(total_seconds // 60)
        secs = int(total_seconds % 60)
        hundredths = int(round((total_seconds - int(total_seconds)) * 100))
        if hundredths >= 100:
            hundredths = 99
        return f"{minutes:02d}:{secs:02d}.{hundredths:02d}"

