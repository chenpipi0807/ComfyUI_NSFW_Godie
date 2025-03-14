import os
import re
import time

class NSFWTextFilter:
    _instance = None
    _nsfw_words = None
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
        if (self._nsfw_words is None or 
            current_time - self._last_load_time > self._cache_duration):
            
            nsfw_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nsfw.txt")
            
            try:
                with open(nsfw_file_path, 'r', encoding='utf-8') as f:
                    # Strip whitespace and filter out empty lines
                    self._nsfw_words = set(word.strip().lower() for word in f.readlines() if word.strip())
                self._last_load_time = current_time
                print(f"[NSFW Filter] Loaded {len(self._nsfw_words)} words")
            except Exception as e:
                print(f"[NSFW Filter] Error loading NSFW words: {e}")
                # If loading fails, make sure we have at least an empty set
                if self._nsfw_words is None:
                    self._nsfw_words = set()
    
    def filter_text(self, text):
        """Filter NSFW words in text while preserving original formatting"""
        if not text:
            return text
            
        # Reload words if needed
        self.load_nsfw_words()
        
        # Create a case-preserving mapping of words to filtered versions
        result = text
        
        # Strategy: split by common delimiters while preserving them
        delimiters = r'([,.!?\s\-_:;\(\)\[\]\{\}"\'/\\|<>@#$%^&*+=~`])'
        tokens = re.split(delimiters, text)
        
        # Process each token
        for i, token in enumerate(tokens):
            if token.strip() and not re.match(delimiters, token):
                # Check if the lowercase version of the token is in the NSFW list
                if token.lower() in self._nsfw_words:
                    # Replace with asterisks while preserving length
                    tokens[i] = '*' * len(token)
        
        # Rejoin the tokens
        return ''.join(tokens)


class NSFWFilterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "filter_nsfw"
    CATEGORY = "text"
    OUTPUT_NODE = True
    DISPLAY_NAME = "ComfyUI_NSFW_Godie"

    def filter_nsfw(self, text):
        filter_instance = NSFWTextFilter.get_instance()
        filtered_text = filter_instance.filter_text(text)
        return (filtered_text,)


# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "NSFWFilterNode": NSFWFilterNode,
}

# Display names for the ComfyUI interface
NODE_DISPLAY_NAME_MAPPINGS = {
    "NSFWFilterNode": "ComfyUI_NSFW_Godie",
}
