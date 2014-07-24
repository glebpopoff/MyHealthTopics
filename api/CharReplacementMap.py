import re

#used for HTML cleanup and language translation
#the tags are stripped when document is translated but we need them back

htmlReplacementDictionary = {'<p>':'x123x ','</p>':' x124x', '<li>':'x125x ','</li>':' x126x','<ul>':'x127x ','</ul>':' x128x'}
xmlRecordReplacementDictionary = {'<record>':'x223x ','</record>':' x224x', '<title>':'x225x ','</title>':' x226x','<summary>':'x227x ','</summary>':' x228x'}

#replace HTML tags with dummy replacements
def translate_tags_from_html(text):
	for i, j in htmlReplacementDictionary.iteritems():
		text = text.replace(i, j)
	return text

#replace dummy chars back to HTML counterparts
def translate_tags_to_html(text):
	for i, j in htmlReplacementDictionary.iteritems():
		text = text.replace(j, i)
	return text

#replace XML record tags with dummy replacements
def translate_tags_from_xml_record(text):
	for i, j in xmlRecordReplacementDictionary.iteritems():
		text = text.replace(i, j)
	return text

#replace dummy chars back to XML record counterparts
def translate_tags_to_xml_record(text):
	for i, j in xmlRecordReplacementDictionary.iteritems():
		text = text.replace(j, i)
	return text
	
#remove HTML tags
def remove_html_tags(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)