def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_external_address():
	data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
	print("External IP: "+data["ip"])
	return data["ip"]

def get_internal_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	print("Internal IP: "+s.getsockname()[0])
	return s.getsockname()[0]