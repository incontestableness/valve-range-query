Python library for Query of Valve Servers over a range of IPs
=============================================================

This is a Python 3 port of https://github.com/anshulshah96/valve-range-query. It should support all Valve Source Dedicated Servers (CS:GO, TF2, L4D2).

I don't recommend actually using this due to its inefficiency. I suggest using python-a2s instead. See my project, GLaDOS, for an example implementation of mass scanning with python-a2s. In particular, you may find ketchupbottle.py in the legacy branch interesting.

To install the library run

::

	pip3 install valve-range-query-3


To scan servers in range " <base_ipaddr> . <axlimits> . <aylimits> "

For example scan '172'.'25'.'0-34'.'0.254'

::
	
	from valverangequery import *
	axlimits = [0,35]
	aylimits = [0,255]
	base_ipaddr = "172.25"
	scanner = SourceScanner(timeout = 20.0, axlimits = axlimits, aylimits = aylimits, base_ipaddr="172.25")
	server_list = scanner.scan_servers()


To obtain player info from server having IP <ip>

::
	
	from valverangequery import *
	ip = "172.25.12.121"
	player_query = PlayerQuery(ip)
	player_list= player_query.player()


----

The respose of **SourceScanner** is a dictionary of list of servers

Each list entry "server_obj" will have following key-value pairs:
	
::

	for server_obj in server_list:
		sample_new_dictionary = {
				'map_name' : server_obj['map'],
				'host' : server_obj['host_ip'],				'num_players' : server_obj['numplayers'],
				'max_players' : server_obj['maxplayers'], 	'server_name' : server_obj['name'],
				'game_name' : server_obj['game'],			'folder' : server_obj['folder'],
				'protocol' : server_obj['protocol'],		'num_bots' : server_obj['bots'],
				'num_humans' : server_obj['numplayers'] - server_obj['bots']
		}

----

The respose of **PlayerQuery** is a dictionary of list of players

Each list entry "player_obj" will have following key-value pairs:
	
::
	
	for player_obj in player_list:
		sample_new_dictionary = {
				'score' : player_obj['score'], 'duration' : int(player_obj['duration'])	, 
				'name'	: player_obj['name']
		}
