import json


class Stat:
    def make_note(self, host):
        with open('data.json', 'r') as f:
            json_string = f.read()
        try:
            dict = json.loads(json_string)
        except:
            print('ушло в ошибку')
            dict = {}
        if host in dict.keys():
            dict[host] += 1
        else:
            dict[host] = 1
        with open('data.json', 'w') as f:
            json.dump(dict, f, indent=2)
