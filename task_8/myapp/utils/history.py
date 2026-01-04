from datetime import datetime, timedelta

class RateHistory:
    def __init__(self):
        self._data = {}

    def add(self, code: str, value: float, ts: datetime | None = None):
        ts = ts or datetime.now()
        self._data.setdefault(code, []).append((ts, float(value)))
        self._prune(code)

    def last_n_days(self, code: str, days: int = 90):
        cutoff = datetime.now() - timedelta(days=days)
        return [(t, v) for (t, v) in self._data.get(code, []) if t >= cutoff]

    def _prune(self, code: str):
        # держим примерно 120 дней “на всякий”
        cutoff = datetime.now() - timedelta(days=120)
        self._data[code] = [(t, v) for (t, v) in self._data.get(code, []) if t >= cutoff]
