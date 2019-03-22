import requests
import json
import time

Slee = 2

token = 'VK API token'
group = 'casual_ukraine2013'
vers = '5.52'
proxy = 'Proxy'


def get_member_list(group, vers, token, offset, proxy):
	print(offset)
	get_membeer_URL = 'https://api.vk.com/method/groups.getMembers?group_id='+group+'&v='+vers+'&access_token='+token+'&fields=connections&offset='+offset
	try:
		r = requests.get(get_membeer_URL, proxies={'http':'http://'+proxy, 'https':'http://'+proxy}, timeout=10)
	except Exception as e:
		print(e)
		time.sleep(Slee)
		return get_member_list(group, vers, token, offset, proxy)

	if str(r) == '<Response [200]>':
		return r
	else:
		print(r)
		time.sleep(Slee)
		return get_member_list(group, vers, token, offset, proxy)

def get_inst_id(username):
	try:
		r = requests.get('https://www.instagram.com/' + username, timeout=10)
	except Exception as e:
		print(e)
		time.sleep(Slee)
		return get_inst_id(username)

	if str(r)=='<Response [404]>':
		return False

	if str(r) == '<Response [200]>':
		r = r.text
		v1 = r.find('profilePage_') + 12
		v2 = r.find('"',v1)
		return r[v1:v2]

	else:
		print(r)
		time.sleep(Slee)
		return get_inst_id(username)

if __name__ == '__main__':
	f = open('Instagram.txt', 'a')

	my_count = 1
	while True:
		r = get_member_list(group, vers, token, str(my_count), proxy)
		json = r.json()
		for x in range(1000):
			try:
				inst = json.get('response').get('items')[x].get('instagram')
			except Exception:
				my_count = 1
				break
			if inst != None:
				print(inst)
				inst_id = get_inst_id(inst)
				if inst_id:
					print(inst_id)
					f.write(inst_id + '\n')
				else:
					print('Username error')
		if my_count == 1:
			break
		my_count = my_count + 1000

	f.close()