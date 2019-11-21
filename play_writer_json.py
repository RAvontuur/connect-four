import json

class PlayWriterJson:

    def __init__(self):
        self.dict = {}

    def close(self):
        pass

    def write_play(self, env, value, visits, q, parent_node):

        if parent_node:
            parent = parent_node.state.get_game_state_short()
        else:
            parent = None

        el = {"parent": parent , "visits": visits, "value": value}
        self.dict[env.get_game_state_short()] = el

    def get_json(self):
        return json.dumps(self.dict)



