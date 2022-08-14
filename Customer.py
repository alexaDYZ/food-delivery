
class Customer():
    def __init__(self, loc,args) -> None:
        self.loc = loc
        self.x = loc[0]
        self.y = loc[1]
        self.args = args