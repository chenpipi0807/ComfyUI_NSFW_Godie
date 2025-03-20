import os
import re
import time

class NSFWTextFilter:
    _instance = None
    _nsfw_words = None
    _nsfw_phrases = None
    _last_load_time = 0
    _cache_duration = 3600  # Cache duration in seconds (1 hour)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NSFWTextFilter()
        return cls._instance

    def __init__(self):
        self.load_nsfw_words()
    
    def load_nsfw_words(self):
        """Load NSFW words from the text file with cache handling"""
        current_time = time.time()
        
        # Check if we need to reload the words
        if (self._nsfw_words is None or self._nsfw_phrases is None or
            current_time - self._last_load_time > self._cache_duration):
            
            nsfw_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nsfw.txt")
            
            try:
                self._nsfw_words = set()
                self._nsfw_phrases = set()
                
                with open(nsfw_file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        term = line.strip().lower()
                        if not term:
                            continue
                            
                        # Add to appropriate set depending on if it contains spaces
                        if ' ' in term:
                            self._nsfw_phrases.add(term)
                        else:
                            self._nsfw_words.add(term)
                
                self._last_load_time = current_time
                print(f"[NSFW Filter] Loaded {len(self._nsfw_words)} single words and {len(self._nsfw_phrases)} phrases")
            except Exception as e:
                print(f"[NSFW Filter] Error loading NSFW words: {e}")
                # If loading fails, make sure we have at least empty sets
                if self._nsfw_words is None:
                    self._nsfw_words = set()
                if self._nsfw_phrases is None:
                    self._nsfw_phrases = set()
    
    def filter_text(self, text, replacement_char='*'):
        """Filter NSFW words in text while preserving original formatting"""
        if not text:
            return text
            
        # Reload words if needed
        self.load_nsfw_words()
        
        # Make a copy of the original text that we'll modify
        result = text
        
        # First, handle phrases (with spaces)
        if self._nsfw_phrases:
            for phrase in self._nsfw_phrases:
                # Case-insensitive search using regex
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                
                def replace_phrase(match):
                    matched_text = match.group(0)
                    return replacement_char * len(matched_text)
                
                result = pattern.sub(replace_phrase, result)
        
        # Now handle single words using the token approach
        # Strategy: split by common delimiters while preserving them
        delimiters = r'([,.!?\s\-_:;\(\)\[\]\{\}"\'/\\|<>@#$%^&*+=~`])'
        tokens = re.split(delimiters, result)
        
        # Process each token
        for i, token in enumerate(tokens):
            if token.strip() and not re.match(delimiters, token):
                # Check if the lowercase version of the token is in the NSFW list
                if token.lower() in self._nsfw_words:
                    # Replace with specified character while preserving length
                    tokens[i] = replacement_char * len(token)
        
        # Rejoin the tokens
        return ''.join(tokens)


class NSFWFilterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
            "optional": {
                "replacement_char": ("STRING", {"default": "*", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "filter_nsfw"
    CATEGORY = "text"
    OUTPUT_NODE = True
    DISPLAY_NAME = "ComfyUI_NSFW_Godie"

    def filter_nsfw(self, text, replacement_char="*"):
        # Make sure replacement_char is not empty, default to '*' if it is
        if not replacement_char:
            replacement_char = "*"
        # If the replacement_char is longer than 1 character, just use the first character
        if len(replacement_char) > 1:
            replacement_char = replacement_char[0]
            
        filter_instance = NSFWTextFilter.get_instance()
        filtered_text = filter_instance.filter_text(text, replacement_char)
        return (filtered_text,)


# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "NSFWFilterNode": NSFWFilterNode,
}

# Display names for the ComfyUI interface
NODE_DISPLAY_NAME_MAPPINGS = {
    "NSFWFilterNode": "ComfyUI_NSFW_Godie",
}
