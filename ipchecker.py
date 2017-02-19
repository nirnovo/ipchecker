# __author__ = 'nir'

import argparse
import requests
import termcolor
import pygeoip

parser = argparse.ArgumentParser(prog='tbip')
parser.add_argument('ip')
ps = vars(parser.parse_args())

indent = ' ' * 8
tb_url = 'http://ip.taobao.com/service/getIpInfo.php?ip='
ipinfo_url = 'http://ipinfo.io/'


def get_ipinfo(url, ip):
    r = requests.get(url + ip)
    return r.json()


def output_result(output, result_arr):
    print(output.ljust(13) + ':' + indent + str(result_arr))


def print_head(title):
    print('\n')
    print(title)
    print('=' * 34)


ua = {'User-Agent': 'curl/7.51.0'}
termcolor.cprint(requests.get('http://ip.cn', headers=ua).text, 'red')
termcolor.cprint('查询IP: ' + ps['ip'], 'yellow')
result = get_ipinfo(tb_url, ps['ip'])

if not result['code']:
    print('=' * 34)
    data = result['data']
    for k, v in data.items():
        output_result(k, v)

else:
    termcolor.cprint('查询失败!', 'yellow')

print_head('GeoLiteCity Result: ')

gi = pygeoip.GeoIP('/Users/nir/Documents/coding/GeoLiteCity.dat')
result = gi.record_by_addr(ps['ip'])
if result != None:
    for k, v in result.items():
        output_result(k, str(v))
else:
    print("No more info!")

print_head('IPinfo.io Result: ')
ipinfo_data = get_ipinfo(ipinfo_url, ps['ip'])
for k, v in ipinfo_data.items():
    output_result(k, v)
