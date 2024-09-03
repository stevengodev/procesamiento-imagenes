import os
import threading

class FileProducer(threading.Thread):
    def __init__(self, queue, directory):
        super().__init__()
        self.queue = queue
        self.directory = directory



    def run(self):
        self.process_directory(self.directory)



    def process_directory(self, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.queue.put(file_path)
                print(f"Producer added: {file_path}")
