"""
Keyword extraction utilities.

Extracts meaningful keywords, n-grams, and topics from text content.
"""

import re
from collections import Counter
from typing import List, Set, Tuple
import string


class KeywordExtractor:
    """
    Extract keywords and n-grams from text with stopword filtering.
    
    Simple implementation without external dependencies.
    For production, consider using libraries like spaCy, NLTK, or KeyBERT.
    """
    
    # Common English stopwords
    STOPWORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
        'what', 'when', 'where', 'who', 'which', 'why', 'how', 'or', 'if',
        'do', 'does', 'did', 'not', 'can', 'could', 'would', 'should', 'may',
        'might', 'must', 'shall', 'i', 'you', 'we', 'my', 'your', 'his',
        'her', 'their', 'our', 'been', 'being', 'am', 'were', 'just', 'about',
        'into', 'than', 'more', 'also', 'very', 'so', 'such', 'get', 'got',
        'make', 'made', 'go', 'went', 'come', 'came', 'see', 'saw', 'know',
        'knew', 'think', 'thought', 'take', 'took', 'give', 'gave', 'tell',
        'told', 'now', 'then', 'here', 'there', 'all', 'any', 'some', 'no',
        'yes', 'one', 'two', 'three', 'first', 'last', 'other', 'another',
        'each', 'every', 'few', 'many', 'much', 'most', 'several', 'both',
        'either', 'neither', 'same', 'different', 'new', 'old', 'good', 'bad',
        'big', 'small', 'long', 'short', 'high', 'low', 'up', 'down', 'over',
        'under', 'above', 'below', 'before', 'after', 'between', 'during',
        'through', 'out', 'back', 'off', 'around', 'away', 'still', 'since'
    }
    
    def __init__(self, additional_stopwords: Set[str] = None):
        """
        Initialize keyword extractor.
        
        Args:
            additional_stopwords: Additional words to filter out
        """
        self.stopwords = self.STOPWORDS.copy()
        if additional_stopwords:
            self.stopwords.update(additional_stopwords)
    
    def extract_keywords(self, text: str, top_n: int = 10, min_length: int = 3) -> List[str]:
        """
        Extract top keywords from text.
        
        Args:
            text: Input text
            top_n: Number of top keywords to return
            min_length: Minimum word length to consider
            
        Returns:
            List of top keywords sorted by frequency
        """
        # Tokenize and clean
        words = self._tokenize(text, min_length)
        
        # Count frequencies
        word_freq = Counter(words)
        
        # Return top N
        return [word for word, count in word_freq.most_common(top_n)]
    
    def extract_bigrams(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract top bigrams (2-word phrases) from text.
        
        Args:
            text: Input text
            top_n: Number of top bigrams to return
            
        Returns:
            List of top bigrams sorted by frequency
        """
        words = self._tokenize(text, min_length=2)
        
        # Generate bigrams
        bigrams = []
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            bigrams.append(bigram)
        
        # Count frequencies
        bigram_freq = Counter(bigrams)
        
        # Return top N
        return [bigram for bigram, count in bigram_freq.most_common(top_n)]
    
    def extract_trigrams(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract top trigrams (3-word phrases) from text.
        
        Args:
            text: Input text
            top_n: Number of top trigrams to return
            
        Returns:
            List of top trigrams sorted by frequency
        """
        words = self._tokenize(text, min_length=2)
        
        # Generate trigrams
        trigrams = []
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
            trigrams.append(trigram)
        
        # Count frequencies
        trigram_freq = Counter(trigrams)
        
        # Return top N
        return [trigram for trigram, count in trigram_freq.most_common(top_n)]
    
    def extract_ngrams(self, text: str, n: int = 2, top_n: int = 10) -> List[str]:
        """
        Extract top n-grams from text.
        
        Args:
            text: Input text
            n: Size of n-grams (2 for bigrams, 3 for trigrams, etc.)
            top_n: Number of top n-grams to return
            
        Returns:
            List of top n-grams sorted by frequency
        """
        words = self._tokenize(text, min_length=2)
        
        # Generate n-grams
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = " ".join(words[i:i+n])
            ngrams.append(ngram)
        
        # Count frequencies
        ngram_freq = Counter(ngrams)
        
        # Return top N
        return [ngram for ngram, count in ngram_freq.most_common(top_n)]
    
    def _tokenize(self, text: str, min_length: int = 3) -> List[str]:
        """
        Tokenize text into clean words.
        
        Args:
            text: Input text
            min_length: Minimum word length
            
        Returns:
            List of clean, lowercase words
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove punctuation and special characters
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split into words
        words = text.split()
        
        # Filter: remove stopwords, short words, numbers
        filtered_words = [
            word for word in words
            if len(word) >= min_length
            and word not in self.stopwords
            and not word.isdigit()
        ]
        
        return filtered_words
    
    def get_keyword_stats(self, text: str) -> Tuple[List[str], List[str], List[str]]:
        """
        Get comprehensive keyword statistics.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (keywords, bigrams, trigrams)
        """
        keywords = self.extract_keywords(text, top_n=15)
        bigrams = self.extract_bigrams(text, top_n=10)
        trigrams = self.extract_trigrams(text, top_n=5)
        
        return keywords, bigrams, trigrams
