# Hiroki Yun
# V00687838

import sys
import json

def main():
	
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = {}

    for line in sent_file:
        term, score = line.split("\t") # The file is tab-delimited.
        scores[term] = int(score) 

    # A dictionary to store total score for each state in US
    state_score = {}

    # Read every line on tweet_file.  
    for line in tweet_file.readlines():
        # Decode each line of JSON in live stream data
        decoded_line = json.loads(line) 

        try:
            tweet_msg = decoded_line['text'].encode('utf-8')
            if decoded_line['lang'] != "en":
                continue
            try:
                if decoded_line['place']['country_code'] != "US":
                    continue

                tweet_str_list = tweet_msg.split() # Split a tweet into a set of strings
                term_score_list = [] # A list of score for each term in one tweet

                # Calculate the sum for a tweet
                for word in tweet_str_list:
                    try:
                        term_score = float(scores[word.lower()])
                    except KeyError:
                        term_score = 0.0
                    term_score_list.append(term_score)

                # Obtain originated state
                state_ab = decoded_line['place']['full_name'].split()[-1]

                # Add tweet score for the state
                try:
                    state_score[state_ab] += sum(term_score_list)
                except KeyError:
                    state_score[state_ab] = sum(term_score_list)

            except TypeError:
                pass # Ignore tweets with no place information (Object type = None)

        except KeyError:
            pass # Ignore deleted lines

    # Output the happiest state
    print max(state_score, key = lambda x: state_score.get(x))

if __name__ == '__main__':
    main()
