#!/usr/bin/env python2
# -*- encoding: utf8 -*-

import re
import requests
import argparse
import traceback

from bs4 import BeautifulSoup

class KernelTool:

	# 获取所有的URL
	def get_links(self, link, regex, **kwargs):
		data = []

		try:
			resp = requests.get(link)
			for line in resp.text.split("\n"):
				match = re.search('href="([^"]+)', line)
				if not match:
					continue

				if re.match(regex, match.group(1)):
					data.append(link + match.group(1))
		except Exception as e:
			traceback.print_exc()
			pass

		return data

	def deb_ubuntu(self):
		links = self.get_links(
			'http://archive.ubuntu.com/ubuntu/pool/main/l/linux/',
			'^linux-headers-4\\.(4|15)\\.0-\\d+(-generic|_4\\.(4|15)).*_(all|amd64).deb'
		)

		self.do_print(links)

	# 获取所有 centos 版本号
	def get_centos_release(self, **kwargs):
		data = []
		try:
			resp = requests.get('http://vault.centos.org/')
			soup = BeautifulSoup(resp.text, "html.parser")
			for a in soup.select('td a[href]'):
				href = a.attrs['href'].replace('/', '')
				if href.startswith('6.') or href.startswith('7.'):
					data.append(href)
		except Exception as e:
			print e
			pass

		return data

	# 从 Packages 目录提取需要的 rpm 下载地址
	# http://vault.centos.org/6.0/os/x86_64/Packages/
	def get_rpm_link(self, link, **kwargs):
		return self.get_links(link, '^kernel-(2|3|4|headers|devel).*\\.x86_64\\.rpm$')

	def do_print(self, data):
		for row in data:
			print 'wget -c', row

	def rpm_latest(self):
		print "\n# centos 6 latest"
		self.do_print(
			self.get_rpm_link('http://mirrors.163.com/centos/6/os/x86_64/Packages/') +
			self.get_rpm_link('http://mirrors.163.com/centos/6/updates/x86_64/Packages/'))
		
		print "\n# centos 7 latest"
		self.do_print(
			self.get_rpm_link('http://mirrors.163.com/centos/7/os/x86_64/Packages/') +
			self.get_rpm_link('http://mirrors.163.com/centos/7/updates/x86_64/Packages/'))

		print "\n# centos 8 latest"
		self.do_print(
			self.get_rpm_link('http://mirrors.163.com/centos/8/BaseOS/x86_64/os/Packages/') +
			self.get_rpm_link('http://mirrors.163.com/centos/8-stream/BaseOS/x86_64/os/Packages/'))

		print "\n"

	def rpm_archive(self):
		for rel in self.get_os_release():
			print "\n# centos ", rel
			self.do_print(self.get_rpm_link('http://vault.centos.org/' + rel + '/os/x86_64/Packages/'))

			print "\n# centos ", rel, 'updates'
			self.do_print(self.get_rpm_link('http://vault.centos.org/' + rel + '/updates/x86_64/Packages/'))

	def rpm_source():
		for rel in self.get_os_release():
			print "\n# ", rel
			self.do_print(self.get_rpm_link('http://vault.centos.org/' + rel + '/os/Source/SPackages/'))

			print "\n# ", rel, 'updates'
			self.do_print(self.get_rpm_link('http://vault.centos.org/' + rel + '/updates/Source/SPackages/'))

def main():	
	parser = argparse.ArgumentParser(description='kernel fetch tools')
	parser.add_argument('-a', dest='all', default = False, action='store_true', help='Fetch archived RPM packages')
	parser.add_argument('-s', dest='source', default = False, action='store_true', help='Fetch source RPM instead')
	parser.add_argument('-o', dest='os', default = 'centos', help='Specify OS type')

	args = parser.parse_args()
	kern = KernelTool()

	try:
		if args.os == 'ubuntu':
			kern.deb_ubuntu()
		elif args.os == 'centos':
			if args.source:
				kern.rpm_source()
			else:
				kern.rpm_latest()
				if args.all:
					kern.rpm_archive()
	except KeyboardInterrupt:
		pass
	except Exception as e:
		raise

if __name__ == '__main__':
	main()



