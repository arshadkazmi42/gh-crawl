import time


class ProcessTime:


    def __init__(self):

        self.start_time = time.time()


    def start(self):

        self.start_time = time.time()

    
    def stop(self):

        return self.convert_to_minutes((time.time() - self.start_time))

    
    def convert_to_minutes(self, time):

        return (time / 60)
    