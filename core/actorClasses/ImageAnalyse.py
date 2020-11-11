import random
import time


class ImageAnalyse:
    @staticmethod
    def analyse(_id, frame, queue):
        time.sleep(random.uniform(0.2, 0.55))
        queue.put(str('id ' + str(_id) + ': ' + str(frame)))
        return 'id ' + str(_id) + ': ' + str(frame)
