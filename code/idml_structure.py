from os import listdir
from os.path import isfile, join
import parse as p

# harcode leaflet definition, would be a file
TEXT_GENERAL_DIR = "/Users/chus/Dropbox/3plus2/3plus2_text/Lent"
TEXT_SUBDIRS = ["/Lent February/", "/Lent March/", "/Lent April/"]

TEXTS_NUM = 46
TEXT_SUBDIRS_COUNT = [11,31,4]

IDMLFOLDER_FOLDER = "/Volumes/Datos002/WESTPARK/3+2/leaflets_design/idml_decomposition/masPruebas/"
NEWIDMLFOLDER_FOLDER = "/Volumes/Datos002/WESTPARK/3+2/leaflets_design/idml_decomposition/lent_leaflet/"
STORIES_FOLDER = "Stories"
NEW_STORIES_FOLDER = "newStories"

mypath = IDMLFOLDER_FOLDER+STORIES_FOLDER+"/"
outPath = NEWIDMLFOLDER_FOLDER+STORIES_FOLDER+"/"


def setContent(inCitFileName, outCitFileName, content):
	inCitFile  = open(inCitFileName, 'r')
	outCitFile = open(outCitFileName, 'w')

	inText = inCitFile.read()

	idx1 = inText.find("codigo")

	if idx1 >= 0:
		firstText = inText[0:idx1]
		secondText = inText[idx1+10:]
		inText = firstText+content+secondText

	outCitFile.write(inText)

	inCitFile.close()
	outCitFile.close()

def setMainContent(inCitFileName, outCitFileName, gospelText, commentsText):
	inCitFile  = open(inCitFileName, 'r')
	outCitFile = open(outCitFileName, 'w')

	#read the origin
	iniBlock = 6
	midBlock = 5
	finBlock = 3
	inTextIni = ""
	for f in range(iniBlock) :
		inTextIni = inTextIni + inCitFile.readline()

	for f in range(midBlock) :
		inCitFile.readline()

	inTextFin = ""
	for f in range(finBlock) :
		inTextFin = inTextFin + inCitFile.readline()

	content = ""

	gospelContent = paragraphStyleBlock("cita", characterStyleBlock("contenido_cita", gospelText, True))#+"\t\t\t\t</br>\n")
	content = content + gospelContent

	for parr in range(len(commentsText)) :
		textParrafo = ""
		elementParrafo = commentsText[parr]
		for block in range(len(elementParrafo)) :
			elementBlock = elementParrafo[block]
			textParrafo = textParrafo + characterStyleBlock(elementBlock[0], elementBlock[1])

		content = content + paragraphStyleBlock("normal",textParrafo)


	finalText = inTextIni+content+inTextFin

	outCitFile.write(finalText)

	inCitFile.close()
	outCitFile.close()

def characterStyleBlock(style, content, withspace = False):
	ini = """\t\t\t\t<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/{0}">
			 \t\t<Content>""".format(style)
	fin = """</Content>\n"""
	if withspace : fin = fin + "<br/>"
	fin = fin + "\t</CharacterStyleRange>\n"
	return ini+content+fin

def paragraphStyleBlock(style, content):
	ini = """\t\t\t<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/{0}">\n""".format(style)
	fin = "\t\t\t</ParagraphStyleRange>\n"
	return ini+content+fin

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

allfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

# 1. Read all the stories files and create the relation table
numOfPages = 70
tabla = [{} for i in range(numOfPages)]
used = [False for i in range(numOfPages)]
minPage = int(9999)
maxPage = int(-1)
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
		maxPage = int(pagina)
	if value < minPage : 
		minPage = int(pagina)
	
	#print allfiles[f] + "- pagina: " + pagina + " - bloque: " + bloque

#print "minPage " + str(minPage)
#print "maxPage " + str(maxPage)
#print "textContents " + str(len(textContents))

comments = {}
gospel = {}
citation = {}
days = {}
saints = {}

textId = int(0)
for text in textContents :
	extFile = open(text, 'r')
	items = {}
	for keyword, paragraphs in p.parse_text(extFile.read()) :
		items.update(p.PROCESSORS[keyword](paragraphs))
	extFile.close()

	extFile = open(text, 'r')
	day = extFile.readline()
	saint = extFile.readline()
	items['DAY'] = day[:len(day)-1]
	items['SAINT'] = saint[:len(saint)-1]
	extFile.close()

	#print text
	comments[textId] = items['COMMENTS']
	gospel[textId]   = items['GOSPEL']
	citation[textId] = items['CITATION']
	days[textId] = items['DAY']
	saints[textId] = items['SAINT']
	textId = textId+1


maxPage = int(maxPage)
pageId = 0
for i in range(len(comments)) :
	if i >= minPage :
		#citation
		inCitFileName = mypath+tabla[i]['C']
		outCitFileName = outPath+tabla[i]['C']
		setContent(inCitFileName, outCitFileName, citation[pageId])
		
		#day
		inCitFileName = mypath+tabla[i]['D']
		outCitFileName = outPath+tabla[i]['D']
		setContent(inCitFileName, outCitFileName, days[pageId])

		#saint
		inCitFileName = mypath+tabla[i]['S']
		outCitFileName = outPath+tabla[i]['S']
		setContent(inCitFileName, outCitFileName, saints[pageId])

		#gospel+comments
		inCitFileName = mypath+tabla[i]['T']
		outCitFileName = outPath+tabla[i]['T']
		setMainContent(inCitFileName, outCitFileName, gospel[pageId], comments[pageId])
		pageId = pageId+1

print "Builded " + str(pageId) +" pages!"



