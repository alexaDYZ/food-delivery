import copy


class O():
    def __init__(self, index) -> None:
        self.id = index


ls = [O(1),O(2),O(3),O(4)]
ls_copy = copy.deepcopy(ls)

ls_copy.append(O(1000))
ls_copy[0] = O(-100)

print([e.id for e in ls])
print([e.id for e in ls_copy])
