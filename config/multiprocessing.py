import multiprocessing  
  
class UvicornWorkerRecommender(object):  
    def __init__(self):  
        self.cpu_cores = multiprocessing.cpu_count()  
        self.expected_load = 0  
        self.io_bound = True  
  
    def set_cpu_cores(self, cpu_cores):  
        self.cpu_cores = cpu_cores  
  
    def set_expected_load(self, expected_load):  
        self.expected_load = expected_load  
  
    def set_io_bound(self, io_bound):  
        self.io_bound = io_bound  
  
    def recommend_workers(self):  
        if self.io_bound:
            recommended_workers = self.cpu_cores * 2
        else:
            recommended_workers = self.cpu_cores  
  
        # Adjust based on expected load  
        if self.expected_load > 1000:  # Example threshold for high load  
            recommended_workers *= 2  # Double the recommended workers for high load  
  
        return recommended_workers  