#!/usr/bin/env python3
"""
Simple test script for the ComfyUI_NSFW_Godie functionality.
This can be run directly to test the filter without ComfyUI.
"""

import os
import sys

# Add parent directory to path so we can import the nodes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ComfyUI_NSFW_Godie.nodes import NSFWTextFilter

def test_filter():
    """Test the NSFW filter with some example text."""
    filter_instance = NSFWTextFilter.get_instance()
    
    # Test cases
    test_cases = [
        "This is a normal sentence without any NSFW content.",
        "This sentence contains the word sex which should be filtered.",
        "Mixed case words like SeX and PENIS should also be filtered.",
        "Words with punctuation like sex, penis! and naked? should be filtered.",
        "Multiple words like sex, penis, and naked in one sentence should all be filtered."
    ]
    
    print("NSFW Filter Test Results:")
    print("-" * 50)
    
    for i, test in enumerate(test_cases):
        filtered = filter_instance.filter_text(test)
        print(f"Test {i+1}:")
        print(f"Original: {test}")
        print(f"Filtered: {filtered}")
        print("-" * 50)

if __name__ == "__main__":
    test_filter()
