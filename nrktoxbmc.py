# Imports
import sys
import re
import json
import requests

# Config
hosts = [
    {'name':'kontor', 'host':'192.168.1.10', 'port':'8060', 'user':'xbmc', 'pasw':'xbmc'},
    {'name':'stue', 'host':'192.168.1.11', 'port':'8060', 'user':'xbmc', 'pasw':'xbmc'}
]

# Call XBMC
def call_xbmc(host, stream):
    url = 'http://' + host['host'] + ':' + host['port'] + '/jsonrpc'
    xbmc = requests.get(url + '?request={"jsonrpc":"2.0","id":"1","method":"Player.Open","params":{"item":{"file":"' + stream + '"}}}', auth=(host['user'], host['pasw']))
    
    if xbmc.status_code == 200:
        if xbmc.json()['result'] == 'OK':
            return True
        
    return False

# Get video id
def get_video_id(url):
    # Find video id
    video_id = re.search(r'\/([a-z]{4}[0-9]+)', url)
    
    if video_id:
        if video_id.group(1):
            return video_id.group(1)
    return None

# Get stream url
def get_stream_url(video_id):
    session = requests.session()
    session.headers['User-Agent'] = 'xbmc.org'
    session.headers['X-Requested-With'] = 'XMLHttpRequest'
    session.headers['Cookie'] = "NRK_PLAYER_SETTINGS_TV=devicetype=desktop&preferred-player-odm=hlslink&preferred-player-live=hlslink"

    data = session.get(('http://v7.psapi.nrk.no/mediaelement/%s' % video_id)).json()
    
    return {'available': data['isAvailable'], 'title': data['fullTitle'], 'duration': data['duration'], 'url': data['mediaUrl']}

# Main
if __name__ == '__main__':
    # Header
    print '[NRKtoXBMC]',
    
    # Host
    host = hosts[0]
    
    if len(sys.argv) == 1:
        print '[USAGE] nrktoxbmc.py <nrk_url> [<host_name>]'
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            for h in hosts:
                if h == sys.argv[2]:
                    host = h
        
        # URL
        if sys.argv[1]:
            # Get video id
            video_id = get_video_id(sys.argv[1])
            
            if video_id:
                # Get stream
                stream = get_stream_url(video_id)
                
                if stream['available'] and stream['url']:
                    # Call XBMC
                    #response = call_xbmc(host, stream['url'])
                    response = None
                    
                    if response:
                        print '[OK]', 'Stream sent to XBMC host'
                    else:
                        print '[FAIL]', 'Could not open stream url in XBMC. Wrong XBMC config?'
                else:
                    print '[FAIL]', 'Could not get stream url. Maybe it\'s not available anymore?'
            else:
                print '[FAIL]', 'No video id found. Valid url?'
