import re
from collections import Counter
from datetime import datetime

from get_youtube_info import *
from sub_downloader import *


def execute_youtube_scraper():
    output = []
    print("\n *** YouTube Channel Word Analyzer ***\n\n")
    text = "\n\n *** YouTube Channel Word Analyzer ***\n\n"
    output.append(text)

    channel_filter = input("Provide your desire YouTube channel name or id: ")
    text = "Provide your desire YouTube channel name or id: {}".format(channel_filter)
    output.append(text)

    youtube_ifo = GetYoutubeInfo()
    download = Download()

    # Get channel id
    check_val_1, check_val_2, check_val_3, flag = youtube_ifo.get_channel_info(channel_filter)
    if flag == "error":
        error_domain, error_reason, error_message = check_val_1, check_val_2, check_val_3
        print("Error Domain: {0}".format(error_domain))
        print("Error Reason: {0}".format(error_reason))
        print("Error Message: {0}\n".format(error_message))
    else:
        channel_id, channel_name, logs = check_val_1, check_val_2, check_val_3
        if channel_id:
            print("\n*** Get channel info function log ***\n")
            text = "\n\n*** Get channel info function log ***\n"
            output.append(text)
            for log in logs:
                print(log)
                text = "{}\n".format(log)
                output.append(text)

            print("This {0} channel id is found for this channel {1}.".format(channel_id, channel_name))
            text = "This {0} channel id is found for this channel {1}.".format(channel_id, channel_name)
            output.append(text)

            # Get videos id(s)
            check_val_1, check_val_2, check_val_3, flag = youtube_ifo.get_all_video_ids(channel_id)
            if flag == "error":
                error_domain, error_reason, error_message = check_val_1, check_val_2, check_val_3
                print("Error Domain: {0}".format(error_domain))
                print("Error Reason: {0}".format(error_reason))
                print("Error Message: {0}\n".format(error_message))
            else:
                video_ids, logs = check_val_1, check_val_2
                total_video_id_found = len(video_ids)

                print("\n*** Get all video ids function log ***\n")
                text = "\n\n*** Get all video ids function log ***\n"
                output.append(text)

                for log in logs:
                    print(log)
                    text = "{}\n".format(log)
                    output.append(text)

                print("\nTotal {0} id(s) founded for this {1} channel id.\n".format(total_video_id_found, channel_id))
                text = "\n\nTotal {0} id(s) founded for this {1} channel id.\n".format(total_video_id_found, channel_id)
                output.append(text)

                print("Founded video ids are: {0}.\n".format(" ".join(video_ids)))
                text = "Founded video ids are: {0}.\n".format(" ".join(video_ids))
                output.append(text)

                all_sub_list = []
                successfully_scraped_viveo_ids = []
                unsuccessfully_scraped_viveo_ids = []
                logs = []

                # Download all possible closed captions
                for video_id in video_ids:
                    closed_captions, logs = download.get_closed_captions(video_id, "en")
                    if closed_captions:
                        successfully_scraped_viveo_ids.append(video_id)
                        all_sub_list.append(closed_captions)
                    else:
                        unsuccessfully_scraped_viveo_ids.append(video_id)


                print("\n*** Get closed captions function log ***\n")
                text = "\n\n*** Get closed captions function log ***\n"
                output.append(text)

                for log in logs:
                    print(log)
                    text = "{}\n".format(log)
                    output.append(text)


                no_of_successfully_scraped_viveo_id = len(successfully_scraped_viveo_ids)
                no_of_unsuccessfully_scraped_video_id = len(unsuccessfully_scraped_viveo_ids)

                print("\nTotal videos id(s) found for scrapping: {0}.".format(total_video_id_found))
                text = "\nTotal videos id(s) found for scrapping: {0}.".format(total_video_id_found)
                output.append(text)

                print("\nNo of successfully scraped video id(s): {0}.".format(no_of_successfully_scraped_viveo_id))
                text = "\nNo of successfully scraped video id(s): {0}.".format(no_of_successfully_scraped_viveo_id)
                output.append(text)
                print("Successfully scraped video ids are: {0}.\n".format(" ".join(successfully_scraped_viveo_ids)))
                text = "Successfully scraped video ids are: {0}.\n".format(" ".join(successfully_scraped_viveo_ids))
                output.append(text)

                print("\nNo of unsuccessfully scraped video id(s): {0}.".format(no_of_unsuccessfully_scraped_video_id))
                text = "\nNo of unsuccessfully scraped video id(s): {0}.".format(no_of_unsuccessfully_scraped_video_id)
                output.append(text)
                print("Unsuccessfully scraped video ids are: {0}.\n".format(" ".join(unsuccessfully_scraped_viveo_ids)))
                text = "Unsuccessfully scraped video ids are: {0}.\n".format(" ".join(unsuccessfully_scraped_viveo_ids))
                output.append(text)

                all_sub_str = " ".join(all_sub_list)
                all_sub_str = all_sub_str.lower()
                all_sub_list = re.findall(r"[\w']+", all_sub_str)
                total_words = len(all_sub_list)

                # Calculate word frequency
                sub_word_freq = Counter()
                sub_word_freq.update(all_sub_list)
                sub_word_freq = sub_word_freq.most_common()
                total_unique_words = len(sub_word_freq)

                print("\nTotal {0} word(s) found after successfully scrapping {1} subtitels from given YouTube channel.\n".format(total_words, no_of_successfully_scraped_viveo_id))
                text = "\nTotal {0} word(s) found after successfully scrapping {1} subtitels from given YouTube channel.\n".format(total_words, no_of_successfully_scraped_viveo_id)
                output.append(text)

                print("\nTotal {0} unique word(s) found from {1} word(s).\n".format(total_unique_words, total_words))
                text = "\nTotal {0} unique word(s) found from {1} word(s).\n".format(total_unique_words, total_words)
                output.append(text)

                print("\n*** Top 100 Words Sorted By Maximum Frequency ***\n")
                text = "\n*** Top 100 Words Sorted By Maximum Frequency ***\n"
                output.append(text)

                for i in range(100):
                    print("{0}: {1}".format(sub_word_freq[i][0], sub_word_freq[i][1]))
                    text = "{0}: {1}\n".format(sub_word_freq[i][0], sub_word_freq[i][1])
                    output.append(text)

                search = input("\nWant to find a word frequency? (y/n): ").lower()
                text = "\nWant to find a word frequency? (y/n): {}".format(search)
                output.append(text)

                if search == "y":
                    keyword = input("\nPlease provide your desired keyword: ").lower()
                    text = "\nPlease provide your desired keyword: {}\n".format(keyword)
                    output.append(text)

                    if keyword:
                        for word in sub_word_freq:
                            str_word = word[0].lower()
                            if keyword in str_word:
                                print("{0}: {1}\n".format(word[0], word[1]))
                                text = "{0}: {1}\n".format(word[0], word[1])
                                output.append(text)
                    else:
                        print("\nYou can't perform search with a blank keyword.\n")
                        text = "\nYou can't perform search with a blank keyword.\n"
                        output.append(text)

                print("\n *** Analysis Completed ***\n")
                text = "\n\n *** Analysis Completed ***"
                output.append(text)


                date_time = datetime.now()
                dt_str = date_time.strftime("%d-%b-%Y %H:%M:%S")
                """
                Write closed captions in text a file for further query.
                """
                file_name = "closed_captions_{0}_{1}.txt".format(channel_name, dt_str)
                file = open(file_name,"w")
                file.write(all_sub_str)
                file.close()

                """
                Write terminal output in a text file for further query.
                """
                file_name = "terminal_output_{0}_{1}.txt".format(channel_name, dt_str)
                file = open(file_name,"w")
                for line in output:
                    file.writelines(str(line))
                file.close()
        else:
            print("\n*** Excetion occurred!! No youtube channel found with your provided keyword. ***\n")
            print("Please try again with another valid youtube channel name.\n")

