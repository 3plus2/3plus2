from os import listdir
from os.path import isfile, join
import parse as p

# harcode leaflet definition, would be a file
TEXT_GENERAL_DIR = "/Users/chus/Dropbox/3plus2/3plus2_text/Lent"
TEXT_SUBDIRS = ["/Lent February/", "/Lent March/", "/Lent April/"]

TEXTS_NUM = 46
TEXT_SUBDIRS_COUNT = [11,31,4]

textContents = ["" for i in range(TEXTS_NUM)]
counter = 0
for subdir in TEXT_SUBDIRS :
	Texts_dir = TEXT_GENERAL_DIR+subdir
	partfiles = [ g for g in listdir(Texts_dir) if isfile(join(Texts_dir,g)) ]
	for ff in partfiles :
		#textFile = open(Texts_dir+partfiles[ff], 'r')
		#textContents[counter] = textFile.read()
		textContents[counter] = Texts_dir+ff
		counter = counter+1

IDMLFOLDER_FOLDER = "/Volumes/Datos002/WESTPARK/3+2/leaflets_design/idml_decomposition/test_decomp/"
STORIES_FOLDER = "Stories"

mypath = IDMLFOLDER_FOLDER+STORIES_FOLDER+"/"
allfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

# 1. Read all the stories files and create the relation table
numOfPages = 70
tabla = [{} for i in range(numOfPages)]
used = [False for i in range(numOfPages)]
minPage = 9999
maxPage = -1
for f in range(len(allfiles)) :
	storyFile = open(mypath+allfiles[f], 'r')
	text = storyFile.read()
	pos = text.find("codigo")
	if pos < 0 : continue
	pagina = text[pos+6:pos+9]
	bloque = text[pos+9:pos+10]
	
	value = int(pagina)

	tabla[value][bloque] = allfiles[f]
	used[value] = True
	if value > maxPage : 
		maxPage = pagina
	if value < minPage : 
		minPage = pagina
	
	#print allfiles[f] + "- pagina: " + pagina + " - bloque: " + bloque

print "minPage " + str(minPage)
print "maxPage " + str(maxPage)
print "textContents " + str(len(textContents))

for text in textContents :
	extFile = open(text, 'r')
	items = {}
	for keyword, paragraphs in p.parse_text(extFile.read()) :
		items.update(p.PROCESSORS[keyword](paragraphs))
		print items

