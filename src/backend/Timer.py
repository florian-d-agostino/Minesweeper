import time

class Timer: # !! Use a thread to dont be stuck !!
    def __init__(self): # Init time
        self.time = 0
        self.time_is_running = False

    def reset_time(self): # Set time to 0
        self.time = 0
    
    def start_time(self): # Start the time counter in s 
        self.time_is_running = True
        while self.time_is_running:
            self.time += 1
            time.sleep(1)

    def stop_time(self): # Pause time 
        self.time_is_running = False

    def get_time(self):
        return self.time