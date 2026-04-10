import time

class StopwatchLogic:
    def __init__(self):
        self.start_time = 0
        self.elapsed_before_pause = 0
        self.is_running = False
        self.is_countdown = False
        self.target_seconds = 0
        self.yellow_limit_secs = 0
        self.red_limit_secs = 0

    def set_countdown(self, h, m, s, y_h, y_m, y_s, r_h, r_m, r_s):
        self.target_seconds = (h * 3600) + (m * 60) + s
        self.yellow_limit_secs = (y_h * 3600) + (y_m * 60) + y_s
        self.red_limit_secs = (r_h * 3600) + (r_m * 60) + r_s
        self.is_countdown = True
        self.reset()

    def get_remaining_seconds(self):
        if not self.is_countdown: return 0
        total_elapsed = self.elapsed_before_pause
        if self.is_running:
            total_elapsed += time.time() - self.start_time
        return max(0, self.target_seconds - total_elapsed)

    def get_status(self):
        """Retorna el color y si debe parpadear."""
        rem = self.get_remaining_seconds()
        if rem <= self.red_limit_secs: 
            return "#e74c3c", True  # Rojo + Parpadeo
        if rem <= self.yellow_limit_secs: 
            return "#f1c40f", False # Amarillo
        return "#ecf0f1", False     # Normal

    def toggle_running(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
        else:
            self.elapsed_before_pause += time.time() - self.start_time
            self.is_running = False

    def reset(self):
        self.start_time = 0
        self.elapsed_before_pause = 0
        self.is_running = False

    def get_format_time(self):
        rem = self.get_remaining_seconds()
        return time.strftime("%H:%M:%S", time.gmtime(rem))