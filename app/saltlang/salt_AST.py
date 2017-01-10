
class Part(object):
    pass


class PathPart(Part):
    def __init__(self, parent, me):
        self.parent = parent
        self.me = me

    def __repr__(self):
        return 'PathPart(%s, %s)' % (self.parent, self.me)

    def path(self, l):
        if isinstance(self.parent, PathPart):
            self.parent.path(l)
        else:
            l.append(self.parent)
        l.append(self.me)


class Command(Part):
    def __init__(self, client):
        self.client = client
        self.fun = None
        self.args = []
        self.kwargs = {}

    def setfun(self, fun):
        self.fun = fun

    def getfun(self):
        return self.fun

    def setparams(self, params):
        for param in params:
            param_value = param.value
            if isinstance(param.value, PathPart):
                l = []
                param.value.path(l)
                param_value = '.'.join(l)
            if param.name:
                if param_value == 'True':
                    self.kwargs[param.name] = True
                elif param_value == 'False':
                    self.kwargs[param.name] = False
                else:
                    self.kwargs[param.name] = param_value
            else:
                if param_value == 'True':
                    self.args.append(True)
                elif param_value == 'False':
                    self.args.append(False)
                else:
                    self.args.append(param_value)


class MinionCmd(Command):
    def __init__(self, client, opt, tgt):
        super(MinionCmd, self).__init__(client)
        self.client = client
        if opt:
            self.option = opt
        else:
            self.option = "-C"
        self.target = tgt

    def __repr__(self):
        return 'MinionClient(%s, %s, %s, %s, %s, %s )' % (self.client, self.option, self.target, self.getfun(), self.args, self.kwargs)

    def tojson(self):
        json = {}
        l = []
        self.getfun().path(l)
        json["fun"] = '.'.join(l)
        if len(self.args) > 0:
            json["arg"] = self.args
        if not not self.kwargs:
            json["kwarg"] = self.kwargs
        json["client"] = "local"
        json["tgt"] = self.target
        return json


class MasterCmd(Command):
    def __init__(self, client):
        super(MasterCmd, self).__init__(client)
        self.client = client

    def tojson(self):
        json = {}
        l = []
        self.getfun().path(l)
        json["fun"] = '.'.join(l)
        if len(self.args) > 0:
            if self.client == 'salt-key':
                json['match'] = self.args[0]
            else:
                json["arg"] = self.args
        if not not self.kwargs:
            json["kwarg"] = self.kwargs
        if self.client == "salt-run":
            json["client"] = "runner"
        elif self.client == "salt-key":
            json["client"] = "wheel"
        return json


class Param(Part):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return "param(%s=%s)" % (self.name, self.value)
