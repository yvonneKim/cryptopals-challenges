class Blocks():
    def __init__(self, data, bsize=16):
        if type(data) != bytes:
            data = data.encode('utf-8')

        self.bsize = bsize
        self.block_list = []
        for i in range(0, len(data), bsize):
            self.block_list.append(data[i:i+bsize])

    def get_iterator(self):
        return iter(self.block_list)
