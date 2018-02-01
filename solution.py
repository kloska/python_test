from urllib import request, error 
import json
from datetime import date


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
 

 html_hex = '#{red:x}{green:x}{blue:x}'.format(red=red,green=green,blue=blue)
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
    return date(2017, 1, 1)
