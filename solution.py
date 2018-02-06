from urllib import request, error 
import json
from datetime import datetime, date
import ssl, socket

def sort_list(l):
 """Takes a list and returns a sorted version"""
 l.sort()   
 return l


def rgb_to_hex(red, green, blue):
 """
 Convert red, green, blue values into a HTML hex representation
 The short syntax should (#fff) be used where possible.
 
 '#%02x%02x%02x' % (red, green, blue) 
 """

 red = '{red:x}'.format(red=red)
 green = '{green:x}'.format(green=green)
 blue = '{blue:x}'.format(blue=blue)

 html_hex = '#{0}{1}{2}'.format(red, green, blue) 

 if (len(red) == 2) and (len(green) == 2) and (len(blue) == 2):
  if red[0] == red[1] and green[0] == green[1] and blue[0] == blue[1]:
   html_hex = '#{0}{1}{2}'.format(red[0], green[0], blue[0])
 
 #html_hex = '#{red:x}{green:x}{blue:x}'.format(red=red,green=green,blue=blue)
 return html_hex

def get_github_members(org_name):
 """
 Get the number of (public) members belonging to the specified Github
 organisation
 """
 
 github_url = 'https://api.github.com/orgs/{}/public_members'.format(org_name)
 
 # Returns a http.client.HTTPResponse object
 try:
  response = request.urlopen(github_url)
 except error.HTTPError:
  return -1

 if response.getcode() == 200:
  response_header = response.info()
  if 'link' in response_header:
   link_header_list = response_header['link'].split(';')
   #max pages start index
   i = link_header_list[1].find('page=')
   i += 5
   last_page = int(link_header_list[1][i:-1])

   #count public members from first page 
   data = json.loads(response.read().decode())
   public_members = len(data)

   #perform urlopen() and public members count until last_page reached
   x = 1
   while x <= last_page:
    x += 1
    tmp_github_url = 'https://api.github.com/orgs/{0}/public_members?page={1}'.format(org_name,x)

    response = request.urlopen(tmp_github_url)
    data = json.loads(response.read().decode())
    public_members += len(data)
    
   #return result once loop reached last_page
   return public_members
  else: 
   # Convert bytes from response.read() to str with decode() then to list with json.loads()
   data = json.loads(response.read().decode())
   public_members = len(data)
   return public_members
 else:
  return -1

def get_ssl_expiry(domain):
 """
 Takes a domain and returns a date that represents when the SSL certificate
 will expire.
 """
 
 #Return a new SSLContext object with default settings
 ctx = ssl.create_default_context()
 
 # Create python socket object and return SSL socket
 s = ctx.wrap_socket(socket.socket(), server_hostname=domain) 
 
 # connect to provided address 
 s.connect((domain, 443)) 
 
 # Retreive certificate of destination
 cert = s.getpeercert()

 cert_exp_date = datetime.strptime(cert['notAfter'], '%b %d %X %Y %Z')
 
 s.close() 

 return cert_exp_date.date()
