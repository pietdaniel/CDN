#!/usr/bin/python
import urllib

class hosts:
	def __init__(self):
		self.Origin = 'ec2-54-164-51-70.compute-1.amazonaws.com'
		self.N_Virginia = 'ec2-54-174-6-90.compute-1.amazonaws.com'

	def location(self, ip):
		prefix = 'http://api.hostip.info/get_html.php?ip='
		suffix =  '&position=true'
		response = urllib.urlopen(prefix + ip + suffix).read()
		s = response.splitlines()[0].split(':')[1].strip()
		return s

	def getHost(self, ip):
		print ip
		if self.location(ip) == 'UNITED STATES (US)':
			print self.N_Virginia
		else:
			print 'NO HOST'

h = hosts()
h.getHost('129.10.116.51')