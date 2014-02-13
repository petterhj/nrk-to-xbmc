NRKtoXBMC
============================
Open streams from [NRK](http://tv.nrk.no) in XBMC from the command line. Supports multiple hosts.

**Configuration**  
Enable the webserver in XBMC (Settings->Services->Webserver).  
Open nrktoxbmc.py and edit the list of hosts. First host is default.  
```
hosts = [
    {'name':'kontor', 'host':'localhost', 'port':'8060', 'user':'xbmc', 'pasw':'xbmc'},
    {'name':'stue', 'host':'192.168.1.11', 'port':'8060', 'user':'xbmc', 'pasw':'xbmc'}
]
```

**Usage**
```
python nrktoxbmc.py <stream_url> [<host_name>]
```

**Examples**
```
python nrktoxbmc.py http://tv.nrk.no/program/koif42000307 livingroom
python nrktoxbmc.py http://tv.nrk.no/serie/nedenom-og-hjem/koif31008510/sesong-2/episode-5
```