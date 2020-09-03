# Attempts to parse Titles to find Story Arc Info 
# 
# You are free to modify and distribute this file
##########################################################################
	
GroupKeywords = ["Part","Chapter",": ","Pt.","Pt","Prelude","Conclusion"]

NoStoryArcKey = "---***No Story Arc Found***---"
StoryArcMinimumLength = 6 # seems to be off by one... 
SingleStoryArcMinimumLength = 2

# from CR
def SingleStoryArcFromTitle(metadata, overwrite = False):
	#not books array
	#just one metadata object

	titleArray = []
	titleArray.append(metadata.title)
	storyarc = SingleStoryArcFromTitleArray(titleArray)
	
	if len(storyarc) != 0:
		ProcessAlternateSeries(metadata,storyarc,overwrite)
#end SingleStoryArcFromTitle

	
def SingleStoryArcFromTitleArray(titleArray):
	#test based on number of books selected
	if len(titleArray) > 1:
		#more than 1 book
		storyarc = long_substr(titleArray)
	else:
		#only 1 book - remove part/chapter and everything after
		storyarc = removeGroupKeywordsAndAfter(titleArray[0])
		#print "Story Arc = {0}".format(storyarc)
		#make sure story arc is not the same as the title
		if storyarc == titleArray[0]:
			storyarc = ""
	#endif
	if len(storyarc) < SingleStoryArcMinimumLength:
		storyarc = ""
	
	return storyArc_cleanup(storyarc)




def ProcessAlternateSeries(book,storyarc,overwrite):
	# if there is an alternate series and it is the same as the storyarc name, set alternate series number
	# find number after the groupkeyword, chapter/part number
	lstoryarc = storyarc.lower()
	if book.alternateSeries is not None:
		lAlternateSeries = book.alternateSeries.lower()
	else:
		lAlternateSeries = ""
	#MessageBox.Show(lAlternateSeries.find(lstoryarc).ToString())
	if lAlternateSeries.find(lstoryarc) != -1 and lstoryarc != lAlternateSeries:
		RemoveStoryArcFromAlternateSeries(book,storyarc,overwrite)
	if lstoryarc != lAlternateSeries:
		if overwrite or book.storyArc is None:
			if len(storyarc) > 0:
				book.storyArc = storyarc
	else:
		#don't put found story arc in storyarc field since it is really an alternate series
		#TODO: check title again for another story arc?
		AlternateSeriesNumberHandling(book,storyarc,overwrite)

#end ProcessAlternateSeries
def RemoveStoryArcFromAlternateSeries(book,storyarc,overwrite):
	#remove story arc from AlternateSeries, save it in story arc
	#story arc could be one of several in AlternateSeries
	if overwrite:
		book.alternateSeries = book.alternateSeries.replace(storyarc,"").strip(' ,-(:;')
		
		
		
		#MessageBox.Show(re.sub(re.compile(re.escape(storyarc),re.I),"",book.alternateSeries,0))
		
	#MessageBox.Show(book.alternateSeries)
#end RemoveStoryArcFromAlternateSeries

def AlternateSeriesNumberHandling(book,storyarc,overwrite):
	#find a part number if it exists
	if len(book.alternateSeries) > 0:
		#remove story arc from title
		PartNumber = book.title.replace(storyarc,"").strip().lstrip(',-(:;').strip()
		#MessageBox.Show(PartNumber)
		#remove group keyword, if it exists find first word after it. 
		for Part in GroupKeywords:
			PartNumber = PartNumber.replace("(" + Part, " ")
			PartNumber = PartNumber.replace(Part, " ")
		#take first word left, use that as part number
		PartNumber = PartNumber.strip()
		#MessageBox.Show(PartNumber)
		#MessageBox.Show(PartNumber.find(" ").ToString())
		spaceIndex = PartNumber.find(" ")
		if spaceIndex > -1:
			PartNumber = PartNumber[:PartNumber.find(" ")]
		PartNumber = PartNumber.strip(',-(:;').strip()
		#MessageBox.Show("Alternate Series:\n" + book.alternateSeries + " #" + PartNumber)
		
		if overwrite or book.alternateNumber is None or len(book.alternateNumber) == 0:
			#convert to integer, if error just use text
			try:
				book.alternateNumber = str(text2int(PartNumber))
			except Exception:
				book.alternateNumber = PartNumber
	
				
#end AlternateSeriesNumberHandling


def text2int(textnum, numwords={}):
	textnum = textnum.lower()
	
	if not numwords:
		units = [
		"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
		"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
		"sixteen", "seventeen", "eighteen", "nineteen",
		]

		tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

		scales = ["hundred", "thousand", "million", "billion", "trillion"]

		numwords["and"] = (1, 0)
		for idx, word in enumerate(units):    numwords[word] = (1, idx)
		for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
		for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)



	current = result = 0
	for word in textnum.split():
		if word not in numwords:
			raise Exception("Illegal word: " + word)

		scale, increment = numwords[word]
		current = current * scale + increment
		if scale > 100:
			result += current
			current = 0

	return result + current
	



def makeTitleArray(books):
	titleArray = []
	for book in books:
		#print "%s V%d #%s" % (book.Series , book.Volume , book.Number)
		#print book.title
		#print book.StoryArc
		titleArray.append(book.title)
	
	print(titleArray)
	
	return titleArray		

#http://stackoverflow.com/questions/2892931/longest-common-substring-from-more-than-two-strings-python
# this does not increase asymptotical complexity
# but can still waste more time than it saves.
def shortest_of(strings):
	return min(strings, key=len)

def long_substr(strings):
	#case insensitive
	substr = ""
	if not strings:
		return substr
	reference = shortest_of(strings) #strings[0]
	length = len(reference)
	#find a suitable slice i:j
	for i in xrange(length):
		#only consider strings long at least len(substr) + 1
		for j in xrange(i + len(substr) + 1, length + 1):
			candidate = reference[i:j]  # is the slice recalculated every time?
			if all(candidate.lower() in text.lower() for text in strings):
				substr = candidate
	return substr
	
def prefix_groups(data,method):
	"""Return a dictionary of {prefix:[items]}."""
	lines = data[:]
	groups = dict()
	groups[NoStoryArcKey] = list()
	
	
	if method == 0:
		#remove part and everything after it from title
		removeP = removeGroupKeywordsAndAfter 
	elif method == 1:
		#use alternate Part removal, only remove the word Part from Title
		removeP = removeGroupKeywords
	else:
		#shouldn't call if method is not 0 or 1
		return
		
				
	while lines:
		longest = None
		first = lines.pop()
		
		
		firstNoPart = removeP(first)

		for line in lines:
			prefix = long_substr([firstNoPart, removeP(line)])
			prefix = storyArc_cleanup(prefix)
			#print firstNoPart + "|" + line + "|" + prefix
			if not longest:
				if len(prefix) >= StoryArcMinimumLength:
					#print len(prefix)
					longest = prefix
			elif len(prefix) > len(longest) and len(prefix) >= StoryArcMinimumLength:
				longest = prefix
			#if longest print "longest = " + longest
			#print "prefix = " + prefix

		if longest:
			#group = [first]
			rest = [item for item in lines if longest.lower() in item.lower()]
			#print "rest = " + str(rest)
			[lines.remove(item) for item in rest]
			rest.append(first)
			groups[longest] = rest
			#print "group found = " + longest
		else:
			# Singletons raise an exception
			#raise IndexError("No prefix match for {}!".format(first))
			#print "no Story Arc found for " + first
			#groups[NoStoryArcKey].append(first)
			
			#TODO: do single title check for possible story arc
			single = SingleStoryArcFromTitleArray([first])
			if len(single) == 0:
				groups[NoStoryArcKey].append(first)
			else:
				#should only ever be one title in this group
				groups[single] = list()
				groups[single].append(first)
			#MessageBox.Show(SingleStoryArcFromTitleArray([first]))

	#remove no story arc key if empty list
	if len(groups[NoStoryArcKey]) == 0:
		del groups[NoStoryArcKey]
	return groups


def formatDict(dictionary):
	output = ""
	for k, v in dictionary.items():
		output += k + "\n"
		for item in v:
			output += "\t   " + item + "\n"
		output += "\n"
	
	return output

	
	
def removeGroupKeywords(s):
	processedString = s
	for Part in GroupKeywords:
		processedString = removePart(processedString,Part)
	return processedString
	
def removePart(s,keyword):
	#don't add spaces if already space in keyword
	if keyword.find(" ") == -1:
		keyword = " " + keyword + " "
	partIndex = s.rfind(keyword)
	if partIndex != -1:
		#remove Part from Title
		NoPart = s.replace(keyword," ")
	else:
		NoPart = s
	return NoPart

	
def removeGroupKeywordsAndAfter(s):
	processedString = s
	if s is not None:
		for Part in GroupKeywords:
			processedString = removePartAndAfter(processedString,Part)
	return processedString
	
def removePartAndAfter(s,keyword):
	#don't add spaces if already space in keyword
	if keyword.find(" ") == -1:
		keyword = " " + keyword + " "
	partIndex = s.rfind(keyword)
	if partIndex != -1:
		#remove Part and trailing information from Title
		NoPart = s[:partIndex]
	else:
		NoPart = s
	return NoPart

	
def storyArc_cleanup(storyarc):
	#print "StoryArc before clean up == |" + storyarc + "|"
	#clean up possible StoryArc 
	#remove left over "Part" from books like "Arc Part 1" "Arc Part 2"
	for Part in GroupKeywords:
		storyarc = storyarc.replace(" " + Part, "")
		storyarc = storyarc.replace("(" + Part, "")
	
	#remove whitespace from start and end of string
	storyarc = storyarc.strip()
	
	#remove trailing commas - and ( :
	storyarc = storyarc.rstrip(',-(:')
	
	#remove semi-colon. Used as Story title delimiter
	storyarc = storyarc.strip(';')
	
	#remove whitespace from start and end of string, again
	storyarc = storyarc.strip()
	#print "StoryArc after clean up == |" + storyarc + "|"
	return storyarc
