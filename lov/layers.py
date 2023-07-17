__all__ = ['Layers']


from .laser import *

class Layers:
    def __init__(self, num, lengths, n_list):
        self.num=num
        self.lengths=lengths
        self.n_list=n_list

    def get_num(self):
        return self.num
    def get_n_list(self):
        return self.n_list
    def get_lengths(self):
        return self.lengths

    def propagate_lasers(self, lasers):
        pass



