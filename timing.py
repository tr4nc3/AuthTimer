#!/bin/python
import mechanize
import time
import getopt
import sys
import urllib

class CTimer():
    def __init__(self,url,postdata,userparam,proxy,verbose):
        self.url = url
        self.postdata = postdata
        self.userparam = userparam
        self.proxy = proxy
        self.verbose = verbose
    def FindTimeDiff(self):
        parmvals = self.postdata.split('&')
        parmsdict = dict(s.split('=') for s in parmvals)
        parmsdict[self.userparam] = 'blahahah'  #invalid user
        newpostdata = urllib.urlencode(parmsdict)
        req = mechanize.Request(self.url)
        #req.set_proxy(self.proxy,'http')
        #req.set_proxy(self.proxy,'https')
        # with invalid username
        start_time = time.time()
        resp = mechanize.urlopen(req,newpostdata)
        time_taken1 = time.time() - start_time
        if self.verbose:
            print 'Content-Length: '+str(len(resp.read()))
        req = mechanize.Request(self.url)
        #req.set_proxy(self.proxy,'http')
        #req.set_proxy(self.proxy,'https')
        # with valid username but invalid password
        start_time - time.time()
        resp = mechanize.urlopen(req,self.postdata)
        time_taken2 = time.time() - start_time
        if self.verbose:
            print 'Content-Length: '+str(len(resp.read()))
        return time_taken1, time_taken2

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    cookie = ''
    data = ''
    verbose = False
    qstr = ''
    url = ''
    unameparam = ''
    proxysrv = ''
    
    if argv is None:
        argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(argv[1:], "hu:c:d:p:gvix:", ["help", "url=", "cookie=", "data=", "urlparams=", "get", "verbose","username=","proxy="])
            except getopt.error, msg:
                raise Usage(msg)
                return 2
            print >>sys.stderr, 'Got args'
            for o, a in opts:
                if o in ("-h", "--help"):
                    raise Usage
                if o in ("-u","--url"):
                   url = a
                if o in ("-c","--cookie"):
                   cookie = a
                if o in ("-d","--data"):
                   data = a
                if o in ("-p","--urlparams"):
                   qstr = a
                if o in ("-g","--get"):
                   getreq = True
                if o in ("-v","--verbose"):
                   verbose = True
                if o in ("-i","--username"):
                   unameparam = a
                if o in ("-x","--proxy"):
                   proxysrv = a
            if url is None:
                raise Usage('-u/--url is needed')
            if data is None:
                raise Usage('-d,--data is needed')
            if unameparam is None:
                raise Usage('-i/--username is needed')
            timer = CTimer(url,data,unameparam,proxysrv,verbose)
            for i in xrange(2):
                vals = timer.FindTimeDiff()
                print '(Invalid user time, Valid user time)',vals
                print '   ==> % time difference',(vals[0]/vals[1])*100,'\n'
        except Usage, err:
            print >>sys.stderr, err.msg
            print >>sys.stderr, "for help use --help"
            print >>sys.stderr, 'Usage: ' + argv[0] + ' -u https://www.example.com -d "user=validuser&pwd=invalidpasswd&url=example.com%2ftest"  -i user -x localhost:8080' 
            return 2    
    return 0

if __name__ == "__main__":
    sys.exit(main())