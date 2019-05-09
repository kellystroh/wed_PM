import socket

# For some website return the contents of a tag
# open up a streaming byte connection to the host

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)

class WebRetriever():

    def __init__(self, websiteURL, tag):
        self.URL = websiteURL
        self.tag = tag
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.head = ""
        self.headers = []
        self.content = ""    

    def connector(self):
        print(self.URL)
        self.sock.connect((self.URL, 80)

    def requestInfo(self):
        hostString = "Host: " + self.URL + "\r\n"
        self.sock.send(b"GET / HTTP/1.1\r\n")
        self.sock.send(hostString.encode("ascii"))
        self.sock.send(b"\r\n")

        headbytes = []
        while True:
            chunk = self.sock.recv(1)
            headbytes.append( chunk )
            if b''.join( headbytes[-4:] ) == b'\r\n\r\n':
                break
        self.head = b''.join(headbytes)

    def readHeaders(self):
        lines = self.head.split(b'\r\n')
        # edited line above: changed head to self.head

        status_line = lines[0]
        header_lines = lines[1:]

        for line in header_lines:
            if len(line)==0:
                continue
            colon_index = line.index(b":")
            key = line[:colon_index]
            val = line[colon_index+2:]
            self.headers.append( (key,val) )

    def getContent(self):
        encoding = None
        for key, val in self.headers:
            if key==b"Content-Type":
                charset_subkey = b"charset="
                charset_index = val.index( charset_subkey )
                encoding = val[charset_index+len(charset_subkey):].decode("ascii")
            elif key==b"Content-Length":
                content_length = int(val.decode("ascii"))

        content_bytes = self.sock.recv(content_length)
        self.content = content_bytes.decode(encoding)

    def printTag(self):
        start_tag = "<" + self.tag + ">"
        end_tag = "</" + self.tag + ">"
        start_pos = self.content.index(start_tag)+len(start_tag)
        # edited line above: changed content to self.content
        end_pos = self.content.index(end_tag)
        # edited line above: changed content to self.content

        tagContent = self.content[start_pos:end_pos]
        # edited line above: changed content to self.content

        print(tagContent)


''' 
Kelly comments: When I got this to work, I opened a blank jupyter notebook, 
navigated to the wed_pm directory, and typed "from new import WebRetriever".
In the next cell, I entered the following code:

zeus = WebRetriever("www.example.com","title")
zeus.connector()
zeus.requestInfo()
zeus.readHeaders()
zeus.getContent()
zeus.printTag()
'''
