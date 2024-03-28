class Lending:
    def __init__(self, bcode, rcode, state):
        self.bcode = bcode
        self.rcode = rcode
        # 0: chưa mượn, 1: đã mượn, 2: đã trả
        self.state = state
