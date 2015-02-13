# Hiroki Yun
# V00687838

# Computes the ten most frequently occurring hash tags

import sys
import json
import collections

def main():

	tweet_file = open(sys.argv[1])
	hashtag_pair = {}
        c = collections.Counter()

	for line in tweet_file.readlines():
		decoded_line = json.loads(line)

                try:
                        if decoded_line['lang'] != "en": # Language filter does not work sometimes
                                continue
                        tweet = decoded_line['entities']['hashtags']

                        # Use collections below (not yet used)
                        for hashtag_word in tweet:
                                word = hashtag_word['text'].encode('utf-8')
                                c[word] += 1.0

                except KeyError:
                        pass

        for hashtag_word in c.most_common(10):
                print '%s %0.1f' %(hashtag_word[0], hashtag_word[1])
        

if __name__ == '__main__':
	main()