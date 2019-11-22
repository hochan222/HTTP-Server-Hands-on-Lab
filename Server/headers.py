def parse_headers(rfile):
    """Read from rfile and parse header lines
    :param rfile: input file-like object
    :returns:     parsed header dict 
                  (Keys in the dict are capitalized for convention)
                  (also I dont use '':word'convention of HTTP/2.0 convention or  SPDY just use'word')
    """
    
    headers = {}
    ### Your code here    
    status = rfile.readline().decode("utf-8").split(' ')
    headers['METHOD']=status[0]
    headers['PATH']=status[1]
    headers['VERSION']=status[2].replace('\r\n','')

    while True:
        line = rfile.readline().decode("utf-8").split(':')
        if line[0] == '':
            break
        else:
            headers[line[0].upper()]=line[1].strip().replace('\r\n','')
    return headers