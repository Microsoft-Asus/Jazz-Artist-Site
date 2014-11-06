# build a webscraper for http://www.jazzdisco.org/
# identify the record lable links diffently to treat differently?
# there will be a more involved process for getting at the record lable info...

from bs4 import BeautifulSoup
import requests
import personnelparser

BASE_URL = "http://jazzdisco.org/"

def make_soup(url):
	r = requests.get(url)
	data = r.text
	return BeautifulSoup(data)

def get_category_links(url):
	soup = make_soup(url)
	table = soup.find("table")
	category_links = [BASE_URL + a.get('href') + 'catalog/' for a in table.find_all('a')]
	return category_links

category_links = get_category_links(BASE_URL)
test_page = category_links[0] # Cannonball catalog

class ArtistCatalog():
	
	def __init__(self, artist_url):
		self.artist_url = artist_url
		self.soup = make_soup(self.artist_url)
		self.content = self.soup.find(id="catalog-data")
		self.unicode_list = []
		self.make_unicode_list()

	def make_unicode_list(self):
		c = self.content.prettify()
		s = c.split("<h3>")
		for i in s[1:]:
			if not i.startswith("<h2>"):
				self.unicode_list.append("<h3>" + i)
			else:
				self.unicode_list.append(i)


class Album():

	def __init__(self, album_info):
		self.album_info = album_info
		self.p_strings = []
		self.extract_personnel_strings()
		self.album_dict = {}
		self.create_personnel_dicts()
		
		

	def extract_personnel_strings(self):
		# find first personnel string
		start_1 = self.album_info.index("</h3>") + 5 # tag is 5 characters long
		end_1 = self.album_info.index('<div class="date">')
		p_string_1 = self.album_info[start_1:end_1]
		self.p_strings.append(p_string_1)
		# find second personnel string - will probly be more p_strings for other albums
		copy = self.album_info
		target_string = copy.split("</table>")[1]
		end_2 = target_string.index("<div")
		p_string_2 = target_string[:end_2]
		self.p_strings.append(p_string_2)

	def create_personnel_dicts(self):
		p_string_1 = (self.p_strings[0]).encode('ascii', 'ignore') # convert to ascii
		p_1 = personnelparser.AlbumPersonnel(p_string_1)
		p_1_Album_objects = []
		for a in p_1.final_arrays:
			p_1_Album_objects.append(personnelparser.AlbumArtist(a))
		p_1_Album_dicts = [] # get just the artist_dict attrs
		for a in p_1_Album_objects:
			p_1_Album_dicts.append(a.artist_dict)
		self.album_dict['personnel_1'] = p_1_Album_dicts

		# p_s_2_dicts = []
		# p_string_2 = (self.p_strings[1]).encode('ascii', 'ignore')
		# p_2 = personnelparser.AlbumPersonnel(p_string_2)

x = ArtistCatalog(test_page)
a_i = x.unicode_list[0] # first item (album markup) in unicode list
y = Album(a_i)
z = y.album_dict
a = z['personnel_1']
for d in a:
	print d


		
# content: <div id="catalog-data">
# ( year of recording/age of artist: <h2> )
# personnel string: indicated by newline character in dom - "data"
# recording location/date: <div class="date">
# track titles/catalog num: <table>
	# additional personnel: text data following <table>
	# additional tracks: <table>
	# additional loc/date: <div class="date">

# make album class 
# *(some record info uses "replace" format with personnel for multiple sessions)
# may wish to address age of artist info in catalog tables
	
	# album title, 				ex: Kenny Clarke - Bohemia After Dark
	# album id, 					ex: Savoy MG 12017
	# recording date/location, 		ex: NYC, June 28, 1955
		# multiple sessions?
	# personnel
		# see 'personnel-parser.py'
	# tracks
		# track names
		# track id's
	# additional personnel
	# additional tracks


# make artist class
	
	# artist name
	# albums they've been on