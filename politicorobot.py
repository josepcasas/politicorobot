
''' Use markov chains to make up funny status based on past tweets by politicians '''

import twitter
import unicodecsv
import codecs
import csv
import random
import os.path

#define user
user = 'marianorajoy'


# define the private info
consumer_key='iiNozghJ3ObQNZkzIouS9mMuO'
consumer_secret='cTwo2SYeMj28BZcbPosdovcHCEguvbr0nvVUmuuUXe7N33Z9G9'
access_token_key='3140733411-Rq1mJF8B1YsyreF2DzKf72NTi3GF8JIux3mv2Fu'
access_token_secret='90pTHsNUVsoXisN7IgpgpTFOKDL9Me6nO0HPcbJrfcsWP'

def auth(consumer_key, consumer_secret, access_token_key, access_token_secret):
	return twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret)


def getTweets(user, t):
	i = 0
	max_id = 0
	data = []

	while (i < 3200):
		if (max_id == 0):
			statuses = t.GetUserTimeline(screen_name=user, count=200, include_rts=False)
			for s in statuses:
				data = data + [s.text]

		else:
			statuses = t.GetUserTimeline(screen_name=user, count=200, include_rts=False, max_id = max_id)
			for s in statuses:
				data = data + [s.text]
		
		i = i + 200;
		max_id = statuses[len(statuses)-1].id

	with open("data"+user+".csv", "wb") as f:
		writer = unicodecsv.writer(f, encoding='utf-8')
		for line in data:
			writer.writerow([line])
		f.close()


def cleanData(user):
	f =  open("data"+user+".csv", "rb")
	reader = csv.reader(f)
	data = []
	for line in reader:
		linesplit = line[0].split(None)
		for word in linesplit:
			if word[0:1] == '#':
				linesplit.remove(word)
			if word[0:1] == '@':
				linesplit.remove(word)
			if word[0:2] == '.@':
				linesplit.remove(word)
			if word[0:7] == 'http://':
				linesplit.remove(word)
		data = data + [linesplit]
	return data
		



def createDic(data):

	dic = {}
	for line in data:
		i = 0
		while (i < len(line)-3):
			key = line[i] + ' ' + line[i+1]
			dic[key] = []
			i += 1


	for line in data:
		j = 0
		while (j < len(line)-3):
			key = line[j] + ' ' + line[j+1]
			dic[key] = dic[key] + [line[j+2]]
			j += 1
	return dic



def createSentence(dic):
	nextkey = random.choice(dic.keys())
	k = 0
	sentence = nextkey
	while (nextkey in dic.keys() and len(sentence) < 140 and nextkey[-1:] != '.'):
		sentence = sentence + ' ' + random.choice(dic[nextkey])
		sentenceString = sentence.split(None)
		nextkey = sentenceString[len(sentenceString)-2] + ' ' + sentenceString[len(sentenceString)-1]

	if (sentence[-1:] != '.'):
		sentence = sentence + '.'

	return sentence

def main(user):
	t = auth(consumer_key, consumer_secret, access_token_key, access_token_secret)
	filename = "data"+user+".csv"
	if not os.path.isfile(filename):
		getTweets(user, t)
	data = cleanData(user)
	dic = createDic(data)
	sentence = createSentence(dic)
	status = t.PostUpdate(sentence)
	print sentence
	

if __name__ == "__main__":
    main(user)

















