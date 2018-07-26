import os
import codecs
import collections
import numpy as np 
import unicode_converter as uc
from konlpy.tag import Kkma
from konlpy.utils import pprint

#input_file = os.path.join("input.txt")
input_file = os.path.join("input_littleprince.txt")

with codecs.open(input_file,"r",encoding='cp949') as f:
	data = f.read()

kkma = Kkma()
len_data = len(data)
word_info = kkma.pos(data)

i=0
chars = []
chars_morpheme = []
space_symbol = ' ','P'
linebreak_symbol = '\r\n','LB'
for _ in range(len(word_info)):
	if i == 0:
		chars_morpheme.append(word_info[i][1][0])
		chars.append(word_info[i][0])
	else:
		if not word_info[i][0] in chars:
			chars.append(word_info[i][0])
		if not word_info[i][1][0] in chars_morpheme:
			chars_morpheme.append(word_info[i][1][0])	
	i = i+1	
chars_morpheme.append(space_symbol[1][0])	
chars.append(space_symbol[0])
chars_morpheme.append(linebreak_symbol[1][0])	
chars.append(linebreak_symbol[0])

vocab_size = len(chars)
vocab = dict(zip(chars,range(len(chars))))
vocab_mor_size = len(chars_morpheme)
vocab_mor = dict(zip(chars_morpheme,range(len(chars_morpheme))))

i=0 #word_info index
j=0 #Data index
tensor = []
while 1:

	if i >= len(word_info):
		break

	if data[j] == ' ':
		tensor.append((vocab[' '],vocab_mor['P']))
		j=j+1
		continue
	if data[j] == '\r':
		tensor.append((vocab['\r\n'],vocab_mor['L']))
		j=j+2
		continue
	'''
	if word_info[i][1][0] == 'V':
			temp_word = word_info[i][0]
			temp_word_length = len(temp_word)
			all_component = []
			for s in range(temp_word_length):
				all_component.append(uc.chr_diss(temp_word[s]))
			print(all_component)	
	'''

	temp_word = word_info[i][0]
	temp_word_mor = word_info[i][1][0]
	temp_word_length = len(temp_word)
	if temp_word == data[j:j+temp_word_length]:
		tensor.append((vocab[temp_word],vocab_mor[temp_word_mor]))
		j=j+temp_word_length
		i=i+1
	else:
		## 동사 변형이 문제.
		# bypass method 1

		s = 0
		flag = 0
		while 1:
			s=s+1
			total_search_range = 0
			for k in range(s+1):
				if i+k == len(word_info):
					flag = 2
					break
				total_search_range = total_search_range + len(word_info[i+k][0])
			total_search_range = total_search_range + s #여유분

			if flag == 2:
				break

			for k in range(total_search_range+1):
				bypass_word_length = len(word_info[i+s][0])
				if word_info[i+s][0] == data[j+k:j+k+bypass_word_length]:
					for s2 in range(s):
						tensor.append((vocab[word_info[i+s2][0]],vocab_mor[word_info[i+s2][1][0]]))
					if data[j+k-1:j+k] == ' ':
						tensor.append((vocab[' '],vocab_mor['P']))
					flag = 1
					break
						
			if flag == 1:
				j = j + k
				i = i + s
				break
		'''
		temp_component = uc.chr_diss(data[j])

		component1 = [temp_component[0],temp_component[1],'']
		component2 = ['','',temp_component[2]]

		temp_word1 = uc.chr_ass(component1)
		temp_word2 = uc.chr_ass(component2)
		'''

		'''
		print('//error:there is no word in vocab//')
		print(temp_word)
		print(j)
		print(data[j:j+temp_word_length])
		break
		'''

#print(vocab)
#print(tensor)

'''
tensor = []
i=0
j=0
temp_word = ''
while 1:
	if i+j == len(data):
		break
	temp_word = temp_word + data[i+j]


	if temp_word in chars:
		tensor.append(vocab[temp_word])

		i=i+j+1
		j=0
		temp_word = ''
	else:
		j=j+1
	
print(tensor)
'''