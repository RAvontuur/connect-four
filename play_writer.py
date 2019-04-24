
class PlayWriter:

    def __init__(self, file_name, write=False):
        if write:
            self.f = open(file_name,"w+")
        else:
            self.file_name = file_name

    def close(self):
        self.f.close

    def write_play(self, env, value, visits):
        self.f.write(env.get_game_state_short())
        self.f.write(",")
        self.f.write(str(visits))
        self.f.write(",")
        self.f.write(str(value))
        self.f.write("\n")

    def read_plays(self):
        dict = {}
        with open(self.file_name) as fp:
            for line in fp:
                lst = line.rstrip().split(",")
                el_exist = dict.get(lst[0])
                if el_exist is None:
                    visits1 = 0.0
                    el1 = ['0.0']
                else:
                    visits1 = float(el_exist[0])
                    el1 = el_exist[1:]

                visits2 = float(lst[1])
                el2 = lst[2:]
                for i,item in enumerate(el2):
                    el1[i] = (float(el1[i]) * visits1 + float(el2[i]) * visits2) / (visits1 + visits2)
                el1.insert(0, visits1+visits2)
                dict[lst[0]] = el1
        return dict

    def write_dict(self, dict, file_name):
        with open(file_name, 'w+') as fp:
            fp.write(str(dict))




