#!c:/SDK/Anaconda2/python.exe
#encode:utf-8
from __future__ import print_function
import os, sys
print("PID =", os.getpid())
import argparse
import socket
import subprocess
import ast
from make_colors import make_colors
from pydebugger.debug import debug
#from pause import pause
if sys.version_info == 3:
	raw_input = input
	
class server(object):
	def __init__(self, host='0.0.0.0', port=40000):
		self.host = host
		self.port = port
	
	def bind(self, host=None, port=None):
		if not host:
			host = self.host
		if not port:
			port = self.port
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print(make_colors("Listen On:", 'lc') + make_colors(host, 'lw','bl') + ":" + make_colors(str(port), 'lw','lr'))
		try:
			s.bind((host, port))
			exit = False
			while 1:
				data, address = s.recvfrom(8096)
				if data == 'exit':
					exit = True
					try:
						sys.exit()
					except:
						pass
				if exit:
					break
				debug(data = data)
				debug(address = address)
				#a = os.system(data)
				try:
					process = subprocess.Popen(data, stdout = subprocess.PIPE)
					#(out, err) = process.communicate()
					out = process.stdout
					#print("out =", out.read())
					#print("dir(out) =", dir(out))
					err = process.stderr
					print("OUT SERVER =", out.read())
					debug(out = out.read())
					debug(err = err)
					try:
						err = err.read()
					except:
						pass
					s.sendto(str([str(out.read()), str(err)]), address)
				except:
					os.system(data)
				#if a > 0:
				#	print(make_colors("ERROR", 'lw','lr',['blink']))
		except:
			import traceback
			traceback.format_exc()
			sys.exit()
	
class client(object):
	
	def __init__(self, host='0.0.0.0', port=40000):
		self.host = host
		self.port = port
	
	def send(self, data="TEST", host=None, port=None):
		if not host:
			host = self.host
			if host == '0.0.0.0':
				host = '127.0.0.1'
		if not port:
			port = self.port
		debug(host = host)
		debug(port = port)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.sendto(data, (host, port))
		try:
			data, server = s.recvfrom(8096)
			debug(data = data)
			#data = ast.literal_eval(data)
			print("OUTPUT =", data)
			#print("ERROR  =", data[1])
			#s.close()
			try:
				sys.exit()
			except:
				pass
		except:
			import traceback
			traceback.format_exc()
			print("NO DATA !")
		#finally:
		#	s.close()
	
	
def usage():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-s', '--server', action='store_true', help='Run server')
	parser.add_argument('-b', '--host', action='store', help='Listen address')
	parser.add_argument('-p', '--port', action='store', help='Listen port')
	parser.add_argument('-c', '--client', action='store', help='Send Data')
	
	if len(sys.argv) == 1:
		parser.print_help()
	else:
		args = parser.parse_args()
		if args.server:
			c = server()
			c.bind(args.host, args.port)
		elif args.client:
			c = client()
			c.send(args.client, args.host, args.port)
		else:
			parser.print_help()
	
if __name__ == '__main__':
	usage()