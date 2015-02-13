# Hiroki Yun
# V00687838

import sys
import json

def main():
	# Command line arguments for execution
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = {}

    for line in sent_file:
        term, score = line.split("\t") # The file is tab-delimited.
        scores[term] = int(score) 

    # A list containing sum of score for every tweet
    tweet_score_list = []

    # Read every line on tweet_file.  
    for line in tweet_file.readlines():
        # Decode each line of JSON in live stream data
        decoded_line = json.loads(line) 

        try:
            tweet_msg = decoded_line['text'].encode('utf-8')

            # Assign a score of zero for a tweet written in foreign language
            if decoded_line['lang'] != "en":
                tweet_score_list.append(0.0)
            else:
                tweet_str_list = tweet_msg.split() # Split a tweet into a set of strings
                term_score_list = [] # A list of score for each term in one tweet

                # Calculate the sum for a tweet
                for word in tweet_str_list:
                    try: 
                        term_score = float(scores[word.lower()]) 
                    except KeyError:
                        term_score = 0.0
                    term_score_list.append(term_score)

                # Insert the sum of score for a tweet into the final list
                tweet_score_list.append(sum(term_score_list))
        except KeyError:
            pass # Ignore deleted lines

        

    # Output the final result
    for value in tweet_score_list:
        print str(value)

if __name__ == '__main__':
    main()
