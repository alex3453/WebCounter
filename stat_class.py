import json


class Stat:
    def __init__(self):
        with open('data.json', 'r') as f:
            json_string = f.read()
        try:
            self.stats = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            print('jsondecoder_exeption')
            self.stats = {}

    def save_json(self):
        with open('data.json', 'w') as f:
            json.dump(self.stats, f, indent=2)

    def update_stat(self, request):
        ip = request.remote_addr
        host = request.json['host']
        path = request.json['pathname']
        referrer = request.json['referrer']
        if host not in self.stats.keys():
            self._create_dict_for_new_host(host)

        host_stat = self.stats[host]
        host_stat['total_visits_count'] += 1
        depth = len(list(filter(lambda e: e != '', path.split('/'))))
        host_stat['average_depth'] = (host_stat['average_depth'] * (host_stat['total_visits_count'] - 1) + depth) / \
                                     host_stat['total_visits_count']
        if ip not in host_stat['users_ip_stat'].keys():
            host_stat['unique_users_count'] += 1
        if path != '/':
            if path not in self.stats[host]['paths_visits_stat'].keys():
                self._create_dict_for_new_path(host, path)
            path_stat = self.stats[host]['paths_visits_stat'][path]
            path_stat['total_visits_count'] += 1
            if ip not in path_stat['users_ip_stat'].keys():
                path_stat['unique_users_count'] += 1
            Stat._increment_dict_counter(path_stat['referrer_stat'], referrer)
            Stat._increment_dict_counter(path_stat['users_ip_stat'], ip)
        Stat._increment_dict_counter(host_stat['browsers_stat'], request.headers['Sec-Ch-Ua'].split(', ')[1])
        Stat._increment_dict_counter(host_stat['operation_systems_stat'], request.headers['Sec-Ch-Ua-Platform'])
        Stat._increment_dict_counter(host_stat['languages_stat'], request.headers['Accept-Language'])
        Stat._increment_dict_counter(host_stat['users_ip_stat'], ip)



    def _create_dict_for_new_host(self, host):
        self.stats[host] = {
            'total_visits_count': 0,
            'average_depth': 0,
            'unique_users_count': 0,
            'paths_visits_stat': {},
            'browsers_stat': {},
            'operation_systems_stat': {},
            'languages_stat': {},
            'users_ip_stat': {}
        }

    def _create_dict_for_new_path(self, host, path):
        self.stats[host]['paths_visits_stat'][path] = {
            'total_visits_count': 0,
            'unique_users_count': 0,
            'referrer_stat': {},
            'users_ip_stat': {}
        }

    @staticmethod
    def _increment_dict_counter(dict, key):
        if key == '':
            exit()
        if key in dict.keys():
            dict[key] += 1
        else:
            dict[key] = 1

    def __del__(self):
        self.save_json()
