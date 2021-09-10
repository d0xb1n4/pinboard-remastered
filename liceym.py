class Bell():
    def __init__(self, *args, **kwargs):
        self.args = []
        self.kwargs = kwargs
        for i in args:
            self.args.append(i)

    def print_info(self):
        if self.args or self.kwargs:
            a = []
            keys = sorted(self.kwargs.keys())
            for i in keys:
                a += [i + ': ' + self.kwargs[i]]
            kwargsj = ', '.join(a)
            a = []
            for i in self.args:
                a.append(i)
            argsj = ', '.join(a)
            if argsj and not kwargsj:
                print(argsj)
            elif kwargsj and not argsj:
                print(kwargsj)
            elif kwargsj and argsj:
                print('; '.join([kwargsj, argsj]))
        else:
            print('-')


class BigBell(Bell):
    a = 0

    def sound(self):
        if not self.a:
            print('ding')
            self.a = 1
        else:
            print('dong')
            self.a = 0


class LittleBell(Bell):
    def sound(self):
        print("ding")


class BellTower:
    def __init__(self, *args):
        self.bells = []
        for arg in args:
            self.bells.append(arg)

    def append(self, bell):
        self.bells.append(bell)

    def sound(self):
        for bell in self.bells:
            bell.sound()
        print('...')