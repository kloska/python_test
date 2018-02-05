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

 ctx = ssl.create_default_context()
 s = ctx.wrap_socket(socket.socket(), server_hostname=domain) 
 s.connect((domain, 443)) 
 
 cert = s.getpeercert()

 cert_exp_date = datetime.strptime(cert['notAfter'], '%b %d %X %Y %Z')
 
 s.close() 
 return cert_exp_date.date()
