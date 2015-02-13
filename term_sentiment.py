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

    tweet_score_list = [] # A list containing sum of score for every tweet
    new_term_score = {} # New term's accumulating score
    new_term_count = {} # New term's occurrences

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

                temp_count = {} # Temporary counter for new term occurrences
                # Calculate the sum for a tweet
                for word in tweet_str_list:
                    try:
                        term_score = float(scores[word])
                    except KeyError: # Handle new terms
                        term_score = 0.0
                        try:
                            temp_count[word] += 1.0
                        except KeyError:
                            temp_count[word] = 1.0


                    term_score_list.append(term_score)

                # Insert the sum of score for a tweet into the final list
                tweet_score_list.append(sum(term_score_list))

                # Update score and count for new terms
                for word, count in temp_count.iteritems():
                    try:
                        new_term_score[word] += count*sum(term_score_list)
                    except KeyError:
                        new_term_score[word] = count*sum(term_score_list)
                    try:
                        new_term_count[word] += count
                    except KeyError:
                        new_term_count[word] = count
        except KeyError:
            pass # Ignore deleted lines

    # Calculate final results
    for word, count in new_term_count.iteritems():
        print '%s %0.3f' %(word, new_term_score[word]/count)

if __name__ == '__main__':
    main()
