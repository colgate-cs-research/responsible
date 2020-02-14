import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer

def get_ngrams(text):

    key_phrases_2gram = ["network neutral", "net neutral", "pay prioritization", "throttle traffic", "open internet", "block traffic"] #add throttle traffic? etc. pay prioritization, block throttle
    key_phrases_3gram = ["support net neutral", "practice net neutral", "support network neutral", "practice network neutral", "be net neutral", "be network neutral", "net neutral violation", "network neutral violation", "violate net neutrality", "violate network neutrality", "against net neutrality", "against network neutrality"]

    lem = WordNetLemmatizer()
    #stem = PorterStemmer()

    stop_words = set(stopwords.words("english"))

    # text1 = "We at Cogent support Net Neutrality – no blocking or throttling of traffic, no paid prioritization of traffic, full access to all lawful content on the Internet, and free flowing interconnection among Internet providers."
    # text2 = "Recently, the Federal Communications Commission rescinded its rules enforcing Net Neutrality. We think that is bad for Internet users and for the Internet. Cogent practices net neutrality. We do not prioritize packet transmissions on the basis of the content of the packet, the customer or network that is the source of the packet, or the customer or network that is the recipient of the packet. Where there are network problems such as congestion at interconnection points or fiber cuts we implement network management tools to minimize harm to the users of our network."
    # text3 = "It is Cogent's belief that both the customer and the Internet as a whole are best served if the application layer remains independent from the network. Innovation in the development of new applications is fueled by the individual's ability to reach as many people as possible without regard to complicated gating factors such as tiered pricing or bandwidth structures used by legacy service providers. Applications proliferate in a free market economy which is the Internet today."

    # text = [text1, text2, text3]

    corpus = []
    length_of_text_list = len(text)
    # print(length_of_text_list)
    for i in range(0, length_of_text_list):
        #Remove punctuations
        new_text = re.sub('[^a-zA-Z]', ' ', text[i])
        
        #Convert to lowercase
        new_text = new_text.lower()
        
        #remove tags
        new_text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",new_text)
        
        # remove special characters and digits
        new_text=re.sub("(\\d|\\W)+"," ",new_text)
        
        ##Convert to list from string
        new_text = new_text.replace("neutrality", "neutral")
        new_text = new_text.split()
        
        #Lemmatisation
        #lem = WordNetLemmatizer()
        new_text = [lem.lemmatize(word, pos = "v") for word in new_text if not word in stop_words]
        new_text = " ".join(new_text)
        corpus.append(new_text)


    def get_top_n2_words(corpus, df):
        if df:
            vec1 = CountVectorizer(stop_words=stop_words,
                ngram_range=(2,2), max_features=2000).fit(corpus)
        else: 
            vec1 = CountVectorizer(max_df=0.8,stop_words=stop_words,
                ngram_range=(2,2), max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in     
                    vec1.vocabulary_.items()]
        if not words_freq:
            return [0] * 6
        #words_freq = [word for word in vec1.vocabulary_.items()]
        #print(words_freq[0:10])

        # words_freq =sorted(words_freq, key = lambda x: x[1], 
        #              reverse=True)
        nn_2gram_phrases = [0] * 6
        for idx in range(len(words_freq)):
            #phrase_list.append(words_freq[idx][0])
            if words_freq[idx][0] == key_phrases_2gram[0]:
                nn_2gram_phrases[0] += words_freq[idx][1]
            if words_freq[idx][0] == key_phrases_2gram[1]:
                nn_2gram_phrases[1] += words_freq[idx][1]
            if words_freq[idx][0] == key_phrases_2gram[2]:
                nn_2gram_phrases[2] += words_freq[idx][1]
            if words_freq[idx][0] == key_phrases_2gram[3]:
                nn_2gram_phrases[3] += words_freq[idx][1]
            if words_freq[idx][0] == key_phrases_2gram[4]:
                nn_2gram_phrases[4] += words_freq[idx][1]
            if words_freq[idx][0] == key_phrases_2gram[5]:
                nn_2gram_phrases[5] += words_freq[idx][1]

        #print(phrase_list[0:10])

        #count = 0
        # nn_2gram_phrases = [0] * 2
        # for idx in range(len(key_phrases_2gram)):
        #     if key_phrases_2gram[idx] in phrase_list:
        #         #count += 1
        #         nn_2gram_phrases[idx] += 1
        #print("TWO")

        #print(nn_2gram_phrases)
        return nn_2gram_phrases


    def get_top_n3_words(corpus, df):
        if df:
            vec2 = CountVectorizer(stop_words=stop_words,
                ngram_range=(3,3), max_features=2000).fit(corpus)
        else: 
            vec2 = CountVectorizer(max_df=0.8,stop_words=stop_words,
                ngram_range=(3,3), max_features=2000).fit(corpus)
        bag_of_words2 = vec2.transform(corpus)
        sum_words2 = bag_of_words2.sum(axis=0) 
        words_freq2 = [(word, sum_words2[0, idx]) for word, idx in     
                    vec2.vocabulary_.items()]
        if not words_freq2:
            return [0] * 12
        #print(words_freq2[0:10])
        # words_freq =sorted(words_freq, key = lambda x: x[1], 
        #             reverse=True)
        # phrase_list = []
        # for idx in range(len(words_freq2)):
        #     phrase_list.append(words_freq2[idx][0])
        # #count = 0
        # nn_3gram_phrases = []
        # print(phrase_list[0:10])
        # for phrase in key_phrases_3gram:
        #     if phrase in phrase_list:
        #         #count += 1
        #         nn_3gram_phrases.append(phrase)

        nn_3gram_phrases = [0] * 12
        for idx in range(len(words_freq2)):
            #phrase_list.append(words_freq[idx][0])
            if words_freq2[idx][0] == key_phrases_3gram[0]:
                nn_3gram_phrases[0] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[1]:
                nn_3gram_phrases[1] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[2]:
                nn_3gram_phrases[2] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[3]:
                nn_3gram_phrases[3] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[4]:
                nn_3gram_phrases[4] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[5]:
                nn_3gram_phrases[5] += words_freq2[idx][1]
            if words_freq2[idx][0] == key_phrases_3gram[6]:
                nn_3gram_phrases[6] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[7]:
                nn_3gram_phrases[7] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[8]:
                nn_3gram_phrases[8] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[9]:
                nn_3gram_phrases[9] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[10]:
                nn_3gram_phrases[10] += words_freq2[idx][1]
            elif words_freq2[idx][0] == key_phrases_3gram[11]:
                nn_3gram_phrases[11] += words_freq2[idx][1]
        #print("THREE")
        #print(nn_3gram_phrases)
        return nn_3gram_phrases

    if length_of_text_list == 1:
        two_gram_ans = get_top_n2_words(corpus, True)
        three_gram_ans = get_top_n3_words(corpus, True)
    else:
        two_gram_ans = get_top_n2_words(corpus, False)
        three_gram_ans = get_top_n3_words(corpus, False)

    return two_gram_ans + three_gram_ans




