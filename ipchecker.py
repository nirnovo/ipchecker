#!__author__ = 'nir'

import argparse
import requests
import termcolor
import pygeoip

parser = argparse.ArgumentParser(prog='ip [ip]')
parser.add_argument('ip')
ps = vars(parser.parse_args())
tb_url = 'http://ip.taobao.com/service/getIpInfo.php?ip='
ipinfo_url = 'http://ipinfo.io/'
indent = ' ' * 8


def ip_check(url, ip):
    r = requests.get(url + ip)
    return r.json()


def output_result(output, result_dic):
    print(output.ljust(13) + ':' + indent + result_dic)


def print_head(title):
    print('\n')
    print(title)
    print('=' * 34)

tb_info = ip_check(tb_url, ps['ip'])
data = tb_info['data']
if not tb_info['code']:
    ua = {'User-Agent': 'curl/7.51.0'}
    termcolor.cprint(requests.get('http://ip.cn', headers=ua).text, 'red')
    termcolor.cprint('查询IP: ' + ps['ip'], 'yellow')
    print_head('Taobao Result: ')
    for k, v in data.items():
        output_result(k, v)
else:
    termcolor.cprint('查询失败!', 'yellow')


print_head('GeoLiteCity Result: ')
gi = pygeoip.GeoIP('/Users/nir/Documents/coding/GeoLiteCity.dat')
result = gi.record_by_addr(ps['ip'])
for k, v in result.items():
    output_result(k, str(v))

print_head('IPinfo.io Result: ')

ipinfo = ip_check(ipinfo_url, ps['ip'])
for k, v in ipinfo.items():
    output_result(k, v)
