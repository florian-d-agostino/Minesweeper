import json
import os

class RecordManager:
    FILE_PATH = os.path.join(os.path.dirname(__file__), "score.json")

    @staticmethod
    def _get_records():
        if not os.path.exists(RecordManager.FILE_PATH):
            return {"0": "99:59", "1": "99:59", "2": "99:59"}
        
        try:
            with open(RecordManager.FILE_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"0": "99:59", "1": "99:59", "2": "99:59"}

    @staticmethod
    def _time_to_seconds(time_str):
        try:
            minutes, seconds = map(int, time_str.split(":"))
            return minutes * 60 + seconds
        except (ValueError, AttributeError):
            return 9999

    @staticmethod
    def check_record(level_id, current_seconds):
        """Returns True if current_seconds is a new record for the level_id."""
        records = RecordManager._get_records()
        key = str(level_id - 1)  # Mapping 1,2,3 -> "0","1","2"
        record_str = records.get(key, "99:59")
        record_seconds = RecordManager._time_to_seconds(record_str)
        
        return current_seconds < record_seconds

    @staticmethod
    def update_record(level_id, current_seconds):
        """Updates the record if current_seconds is better. Returns True if updated."""
        if RecordManager.check_record(level_id, current_seconds):
            records = RecordManager._get_records()
            key = str(level_id - 1)
            minutes = current_seconds // 60
            seconds = current_seconds % 60
            records[key] = f"{minutes:02}:{seconds:02}"
            
            try:
                with open(RecordManager.FILE_PATH, "w") as f:
                    json.dump(records, f, indent=4)
                return True
            except IOError:
                return False
        return False
