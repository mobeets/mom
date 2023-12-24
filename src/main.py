import random
import string
import datetime
import numpy as np
import pandas as pd
import json

import nltk
from nltk.corpus import stopwords
STOPWORDS = stopwords.words('english')

# source: https://cryptics.georgeho.org/data/clues
# CLUEFILE = '/Users/mobeets/Downloads/clues.csv'
CLUEFILE = '/Users/mobeets/code/react-crossword-generator/data/clues.txt'
WORDFILE = 'dictionary.json'

MIN_CLUES = 10
MIN_LENGTH = 5
MAX_LENGTH = 5
MAX_TRIES = 5
JOIN_KEY = '|||'

def load_cluefile(cluefile=CLUEFILE):
	# df = pd.read_csv(cluefile)
	# df = df[df.puzzle_name.apply(lambda x: 'cryptic' not in x.lower() if type(x) is str else False) == True]
	df = pd.read_csv(cluefile, sep='\t', header=None, names=['clue', 'answer', 'x', 'y'])
	return df

def partition(xs, condition):
	"""
	split a list into those that match a condition and those that do not
	"""
	good, bad = [], []
	for x in xs:
		good.append(x) if condition(x) else bad.append(x)
	return good, bad

def rm_punctuation(clue):
	"""
	remove punctuation from clue
	"""
	return clue.translate(str.maketrans('', '', string.punctuation))

def get_word_set(clue, min_word_length):
	"""
	split clue into words of min length that are not stopwords
	"""
	ws = rm_punctuation(clue)
	return [x for x in ws.lower().split(' ') if len(x) >= min_word_length and x not in STOPWORDS]

def remove_similar_words(clues, min_word_length=4):
	"""
	get a preferred group of clues that all have unique words
	"""
	keeps = []
	ignores = []
	all_words = set()
	for clue in clues:
		words = get_word_set(clue, min_word_length)
		if any([w in words for w in all_words]):
			ignores.append(clue)
		else:
			keeps.append(clue)
			all_words.update(words)
	return keeps, ignores

def group_clues_by_type(clues):
	quets, clues = partition(clues, lambda clue: clue.endswith('?'))
	metas, clues = partition(clues, lambda clue: ', say' in clue or 'maybe, ' in clue or ', in a way' in clue or ', perhaps' in clue or ', for one' in clue or ', e.g.' in clue)

	order = []
	if quets:
		order.append(quets.pop())
	if quets:
		order.append(quets.pop())
	if metas and len(order) < 2:
		order.append(metas.pop())
	# if metas and len(order) < 2:
	# 	order.append(metas.pop())
	if clues:
		order.extend(clues)
	if quets:
		order.extend(quets)
	if metas:
		order.extend(metas)
	return order

def order_clues(clues):
	keeps, ignores = remove_similar_words(clues)
	clues_A = group_clues_by_type(keeps)
	clues_B = group_clues_by_type(ignores)
	return clues_A# + clues_B

def order_and_filter_clues(outfile='answers_sorted.json', min_count=6):
	answers = load_answers()
	new_answers = []
	for item in answers:
		clues = order_clues(item['clues'])
		if len(clues) >= min_count:
			item['clues'] = clues[:min_count]
			new_answers.append(item)
	json.dump(new_answers, open(outfile, 'w'))

def save_answers(cluefile=CLUEFILE, outfile='targets2.json', min_clues=MIN_CLUES, min_length=MIN_LENGTH, max_length=MAX_LENGTH, dictfile='dictionary.json'):
	df = load_cluefile(cluefile)

	if dictfile:
		words = json.load(open(dictfile))
	else:
		words = []

	answers = []
	for answer, dfc in df.groupby('answer'):
		if len(answer) < min_length or len(answer) > max_length:
			continue
		if any([x not in string.ascii_letters for x in answer]):
			continue
		clues = dfc.clue.values.tolist()
		lenstr = '({})'.format(len(answer))
		clues = list(set([clue.replace(lenstr, '').strip() for clue in clues if type(clue) is str]))
		clues = [c for c in clues if 'across' not in c.lower() and 'down' not in c.lower()]
		if len(clues) < min_clues:
			continue
		if words and answer.lower() not in words:
			continue
		answers.append({'answer': answer, 'clues': clues})

	np.random.shuffle(answers)
	json.dump(answers, open(outfile, 'w'))

def get_answer_and_clues(answers):
	# answers = filter_answers(answers)
	item = random.choice(answers)
	return item['answer'], item['clues']

def load_answers(infile='answers.json'):
	return json.load(open(infile))

def main():
	answers = load_answers()
	answer, clues = get_answer_and_clues(answers)

	print("X"*len(answer))
	for i in range(MAX_TRIES):
		clue = clues.pop()
		print(clue)
		guess = input('Guess {} of {}: '.format(i+1, MAX_TRIES))
		if guess.strip().upper() == answer:
			print("CORRECT!")
			return
	print("YOU LOSE. The correct answer was {}.".format(answer))

if __name__ == '__main__':
	save_answers()
	# main()
