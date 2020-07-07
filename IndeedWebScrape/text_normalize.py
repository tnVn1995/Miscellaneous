## Strip html tag
import re
import nltk
from bs4 import BeautifulSoup
from typing import List
import multiprocessing as mp
import os
from functools import partial
from timeit import default_timer as timer
import numpy as np
import re
import unicodedata
from nltk.stem import PorterStemmer
import spacy
from nltk.tokenize.toktok import ToktokTokenizer

        
CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"}

stopword_list = nltk.corpus.stopwords.words('english')
tokenizer = ToktokTokenizer()
nlp = spacy.load('en_core_web_md')


def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    # [s.extract() for s in soup(['iframe', 'script'])]
    stripped_text = soup.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+', '\n', stripped_text)
    return stripped_text
## Removing accented characters


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

## Contraction expansion
def expand_contractions( text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


## remove special characters
def remove_special_characters( text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text
## Stemmatization

def simple_stemmer( text):
    ps = PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text
## Lemmatization

text = 'My system keeps crashing his crashed yesterday, ours crashes daily'
def lemmatize_text( text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


## remove stop words
def remove_stopwords( text, stopword_list, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text






def normalize_corpus( corpus: List[str], html_stripping: bool=True, contraction_expansion: bool=True,
                    accented_char_removal: bool=True, text_lower_case: bool=True,
                    text_lemmatization: bool=True, text_stemming: bool=False, special_char_removal: bool=True,
                    stopword_removal: bool=True, stopwords:List[str]=stopword_list, remove_digits: bool=True):
    normalized_corpus = []
    # normalize each document in the corpus
    for doc in corpus:
        # strip HTML
        if html_stripping:
            doc = strip_html_tags(doc)
        # remove accented characters
        if accented_char_removal:
            doc = remove_accented_chars(doc)
        # expand contractions
        if contraction_expansion:
            doc = expand_contractions(doc)
        # lowercase the text
        if text_lower_case:
            doc = doc.lower()
        # stemmatize text
        if text_stemming: 
            doc = simple_stemmer(doc)
        # remove extra newlines
        doc = re.sub(r'[\r|\n|\r\n]+', ' ',doc)
        # lemmatize text
        if text_lemmatization:
            doc = lemmatize_text(doc)
        # remove special characters and\or digits
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = remove_special_characters(doc, remove_digits=remove_digits)
        # remove extra whitespace
        doc = re.sub(' +', ' ', doc)
        # remove stopwords
        if stopword_removal:
            doc = remove_stopwords(doc, stopword_list = stopwords, is_lower_case=text_lower_case)
        normalized_corpus.append(doc)
    return normalized_corpus

def normalize_corpus_multi( corpus: List[str], html_stripping: bool=True, contraction_expansion: bool=True,
                    accented_char_removal: bool=True, text_lower_case: bool=True,
                    text_lemmatization: bool=True, text_stemming: bool=False, special_char_removal: bool=True,
                    stopword_removal: bool=True, stopwords:List[str]=stopword_list, remove_digits: bool=True):
        # strip HTML
        if html_stripping:
            doc = strip_html_tags(corpus)
        # remove accented characters
        if accented_char_removal:
            doc = remove_accented_chars(doc)
        # expand contractions
        if contraction_expansion:
            doc = expand_contractions(doc)
        # lowercase the text
        if text_lower_case:
            doc = doc.lower()
        # stemmatize text
        if text_stemming:
            doc = simple_stemmer(doc)
        # remove extra newlines
        doc = re.sub(r'[\r|\n|\r\n]+', ' ',doc)
        # lemmatize text
        if text_lemmatization:
            doc = lemmatize_text(doc)
        # remove special characters and\or digits
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = remove_special_characters(doc, remove_digits=remove_digits)
        # remove extra whitespace
        doc = re.sub(' +', ' ', doc)
        # remove stopwords
        if stopword_removal:
            doc = remove_stopwords(doc, stopword_list = stopword_list, is_lower_case=text_lower_case)
        return doc
def parallel_normalize_corpus( corpus: List[List[str]], n_processes: int=6):
    """[preprocess texts with multi-cores]
    
    Keyword Arguments:
        corpus {List[List[str]]} -- [text document] (default: {True, contraction_expansion: bool=True,accented_char_removal: bool=True, text_lower_case: bool=True,text_lemmatization: bool=True, text_stemming: bool=False, special_char_removal: bool=True,stopword_removal: bool=True, stopwords:List[str]=stopword_list, remove_digits: bool=True):#stripHTMLifhtml_stripping:doc=strip_html_tags(corpus)#removeaccentedcharactersifaccented_char_removal:doc=remove_accented_chars(doc)#expandcontractionsifcontraction_expansion:doc=expand_contractions(doc)#lowercasethetextiftext_lower_case:doc=doc.lower()#stemmatizetextiftext_stemming:doc=simple_stemmer(doc)#removeextranewlinesdoc=re.sub(r'[\r|\n|\r\n]+', ' ',doc)#lemmatizetextiftext_lemmatization:doc=lemmatize_text(doc)#removespecialcharactersand\ordigitsifspecial_char_removal:#insertspacesbetweenspecialcharacterstoisolatethemspecial_char_pattern=re.compile(r'([{.(-)!}])')doc=special_char_pattern.sub(" \1 ", doc)doc=remove_special_characters(doc, remove_digits=remove_digits)#removeextrawhitespacedoc=re.sub(' +', ' ', doc)#removestopwordsifstopword_removal:doc=remove_stopwords(doc, stopword_list = stopword_list, is_lower_case=text_lower_case)returndocdefparallel_normalize_corpus(corpus:List[List[str]]})
        n_processes {int} -- [number of cores to use] (default: {6})
    
    Returns:
        [List[List[str]]] -- [description]
    """    
    start = timer()

    with mp.Pool(n_processes) as p:
        normalize_corpus = p.map(normalize_corpus_multi, corpus)

    print('Took %.4f seconds with %i process(es).' %
            (timer() - start, n_processes))
    return normalize_corpus
