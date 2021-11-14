import json
import datetime


class Stat:
    def __init__(self):
        with open('data.json', 'r') as f:
            json_string = f.read()
        try:
            self.stats = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            print('jsondecoder_exeption')
            self.stats = {
                'total_hosts_stat': {},
                'date_hosts_stat': {}
            }
            self.save_json()

    def save_json(self):
        with open('data.json', 'w') as f:
            json.dump(self.stats, f, indent=2)

    def update_stat(self, request):
        host = request.json['host']
        if host not in self.stats['total_hosts_stat'].keys():
            Stat._create_dict_for_new_host(self.stats['total_hosts_stat'], host)
        host_stat = self.stats['total_hosts_stat'][host]
        Stat._update_host_stat(host_stat, request)
        now_date = datetime.datetime.now().strftime("%d-%m-%Y")
        if now_date not in self.stats['date_hosts_stat'].keys():
            self.stats['date_hosts_stat'][now_date] = {}
            Stat._create_dict_for_new_host(self.stats['date_hosts_stat'][now_date], host)
        host_stat = self.stats['date_hosts_stat'][now_date][host]
        Stat._update_host_stat(host_stat, request)

    @staticmethod
    def _update_host_stat(host_stat, request):
        ip = request.remote_addr
        path = request.json['pathname']
        host_stat['total_visits_count'] += 1
        depth = len(list(filter(lambda e: e != '', path.split('/'))))
        host_stat['average_depth'] = (host_stat['average_depth'] * (host_stat['total_visits_count'] - 1) + depth) / \
                                     host_stat['total_visits_count']
        if ip not in host_stat['users_ip_stat'].keys():
            host_stat['unique_users_count'] += 1
        if path != '/':
            if path not in host_stat['paths_visits_stat'].keys():
                Stat._create_dict_for_new_path(host_stat, path)
            path_stat = host_stat['paths_visits_stat'][path]
            Stat._update_path_stat(path_stat, request)
        Stat._increment_dict_counter(host_stat['browsers_stat'], request.headers['Sec-Ch-Ua'].split(', ')[1])
        Stat._increment_dict_counter(host_stat['operation_systems_stat'], request.headers['Sec-Ch-Ua-Platform'])
        Stat._increment_dict_counter(host_stat['languages_stat'], request.headers['Accept-Language'])
        Stat._increment_dict_counter(host_stat['users_ip_stat'], ip)

    @staticmethod
    def _update_path_stat(path_stat, request):
        ip = request.remote_addr
        referrer = request.json['referrer']
        path_stat['total_visits_count'] += 1
        if ip not in path_stat['users_ip_stat'].keys():
            path_stat['unique_users_count'] += 1
        Stat._increment_dict_counter(path_stat['referrer_stat'], referrer)
        Stat._increment_dict_counter(path_stat['users_ip_stat'], ip)

    @staticmethod
    def _create_dict_for_new_host(dict, host):
        dict[host] = {
            'total_visits_count': 0,
            'average_depth': 0,
            'unique_users_count': 0,
            'paths_visits_stat': {},
            'browsers_stat': {},
            'operation_systems_stat': {},
            'languages_stat': {},
            'users_ip_stat': {}
        }

    @staticmethod
    def _create_dict_for_new_path(host_stat, path):
        host_stat['paths_visits_stat'][path] = {
            'total_visits_count': 0,
            'unique_users_count': 0,
            'referrer_stat': {},
            'users_ip_stat': {}
        }

    @staticmethod
    def _increment_dict_counter(dict, key):
        if key != '':
            if key in dict.keys():
                dict[key] += 1
            else:
                dict[key] = 1

    def __del__(self):
        self.save_json()
