class Node(object):
    pass


class AttrMap(Node):
    def __init__(self, parent, me):
        self.parent = parent
        self.me = me

    def __repr__(self):
        return 'AttrMap(%s, %s)' % (self.parent, self.me)


class Attr(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_attr(self, json):
        json[self.name] = self.value

    def __repr__(self):
        return 'Attr(%s, %s)' % (self.name, self.value)
