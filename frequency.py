# Hiroki Yun
# V00687838

# Compute term frequency histogram of the livestream data

"""The frequency of a term can be calculated with the following formula:
[num of occurrences of the term in all tweets] divided by
[num of occurrences of all terms in all tweets]
Terms here include any English terms appeared in all tweets"""

import sys
import json

def main():

	print "Hello World!"

	# Command line argument
	tweet_file = open(sys.argv[1])

	hist = {}

	# Needs some way to store new terms appeared in every tweet
	# Read every line on tweet_file.  
	for line in tweet_file.readlines():
		decoded_line = json.loads(line) 
		
		# Get a tweet message
		try:

			if decoded_line['lang'] != "en": # Ignore tweets other than English
				continue

			tweet_msg = decoded_line['text'].encode('utf-8')
			tweet_str_list = tweet_msg.split() # Split each string in a message

			# Add a new term to the dictionary or increment occurrence
			for term in tweet_str_list:
				try:
					hist[term] += 1.0
				except KeyError:
					hist[term] = 1.0
		except KeyError: # Skip searching for terms if the current line is a deleted tweet
			pass

	# Use the histogram to compute term frequency
	for key, value in hist.iteritems():
		print '%s %0.4f'%(key, value/(sum(hist.itervalues())*1.0))

if __name__ == '__main__':
	main()

