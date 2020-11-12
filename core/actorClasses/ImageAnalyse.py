import random
import time


class ImageAnalyse:
    @staticmethod
    def analyse(_id, frame, queue):
        time.sleep(random.uniform(0.2, 0.055))
        queue.put(frame)
        queue.task_done()
        return frame
