import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import logging
import json
from collections import defaultdict


# Configure logging
logging.basicConfig(
   filename='auto_complete.log',
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s'
)


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0
        self.jokes = {}

class Trie:
   def __init__(self):
       self.root = TrieNode()
       self.word_locations = defaultdict(set)

   def insert(self, text):
        node = self.root
        for char in text.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

            if text in node.jokes:
                node.jokes[text] += 1  # Increase frequency
            else:
                node.jokes[text] = 1  # First occurrence

        node.is_end = True
        node.frequency += 1

        words = text.lower().split()
        for word in words:
            self.word_locations[word].add(text)  # Store phrase in the search dictionary
    

  
   def get_autocomplete(self, prefix, limit=10):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        # Sort phrases by frequency in descending order
        sorted_phrases = sorted(node.jokes.items(), key=lambda x: x[1], reverse=True)
        
        return [phrase for phrase, freq in sorted_phrases[:limit]]

  
   def search_word(self, word):
       return list(self.word_locations.get(word.lower(), set()))
  
   def to_dict(self, node=None, prefix=""):
       if node is None:
           node = self.root
       return {
           "is_end": node.is_end,
           "frequency": node.frequency,
           "jokes_count": len(node.jokes),
           "children": {
               char: self.to_dict(child, prefix + char)
               for char, child in node.children.items()
           }
       }


class SearchApp:
   def __init__(self, root):
       self.root = root
       self.root.title("Auto-Complete Homework 4")
       self.root.geometry("1000x600")
       self.root.resizable(False, False)


       # Initialize trie and load jokes
       self.trie = Trie()
       self.load_jokes()


       try:
           # Add main title at the top
           self.title_label = ttk.Label(root, text="Auto-Complete Homework 4",
                                      font=('Helvetica', 16, 'bold'))
           self.title_label.pack(pady=30)


           # Create a main container for centered content
           main_container = ttk.Frame(root)
           main_container.pack(expand=True, fill=tk.BOTH, padx=20)


           # First row: Auto-Complete section
           self.search_frame = ttk.Frame(main_container)
           self.search_frame.pack(pady=20, fill=tk.X)


           # Label for auto-complete
           self.auto_complete_label = ttk.Label(self.search_frame, text="Auto-Complete demo:",
                                              font=('Helvetica', 10))
           self.auto_complete_label.pack(side=tk.LEFT, padx=(0, 10))


           self.search_input = ttk.Entry(self.search_frame, width=100)
           self.search_input.pack(side=tk.LEFT, expand=True, fill=tk.X)
           self.search_input.bind('<KeyRelease>', self.on_input_change)


           # Search output display area
           self.display_text = scrolledtext.ScrolledText(main_container, height=5, width=120)
           self.display_text.pack(pady=10, fill=tk.X)


           # Find frame with input and button
           self.find_frame = ttk.Frame(main_container)
           self.find_frame.pack(pady=20, fill=tk.X)


           # Label for search word
           self.search_label = ttk.Label(self.find_frame, text="Search word:",
                                       font=('Helvetica', 10))
           self.search_label.pack(side=tk.LEFT, padx=(0, 10))


           self.find_input = ttk.Entry(self.find_frame, width=100)
           self.find_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))


           self.find_button = ttk.Button(self.find_frame, text="Search",
                                       command=self.search, width=20)
           self.find_button.pack(side=tk.LEFT)


           # Find results display
           self.find_display = scrolledtext.ScrolledText(main_container, height=5, width=120)
           self.find_display.pack(pady=10, fill=tk.X)


           # Bottom buttons frame
           self.button_frame = ttk.Frame(main_container)
           self.button_frame.pack(pady=30)


           self.export_button = ttk.Button(self.button_frame, text="Export Tree",
                                         command=self.export_tree, width=20)
           self.export_button.pack(side=tk.LEFT, padx=10)


           self.quit_button = ttk.Button(self.button_frame, text="Quit",
                                       command=self.quit_app, width=20)
           self.quit_button.pack(side=tk.LEFT, padx=10)


       except Exception as e:
           logging.error(f"Error in initialization: {str(e)}")
           raise


   def load_jokes(self):
       try:
           with open('ChuckNorrisJokes.txt', 'r', encoding='utf-8') as f:
               jokes = f.readlines()
           for joke in jokes:
               joke = joke.strip()
               if joke:
                   self.trie.insert(joke)
       except Exception as e:
           logging.error(f"Error loading jokes: {str(e)}")
           raise


   def compute_auto_complete(self, current_text):
       try:
           if not current_text:
               return []
           return self.trie.get_autocomplete(current_text)
       except Exception as e:
           logging.error(f"Error in computing auto complete: {str(e)}")
           raise


   def on_input_change(self, event):
       try:
           current_text = self.search_input.get()
           display_list = self.compute_auto_complete(current_text)


           # Clear previous content
           self.display_text.delete('1.0', tk.END)


           # Insert each item from the list on a new line
           for item in display_list:
               self.display_text.insert(tk.END, f"{item}\n")


       except Exception as e:
           logging.error(f"Error in input change handler: {str(e)}")


   def perform_search(self, search_text):
       try:
           if not search_text:
               return []
           return self.trie.search_word(search_text)
       except Exception as e:
           logging.error(f"Error in perform_search: {str(e)}")
           raise


   def search(self):
       try:
           search_text = self.find_input.get()
           display_list = self.perform_search(search_text)


           # Clear previous content
           self.find_display.delete('1.0', tk.END)


           # Insert each item from the list on a new line
           for item in display_list:
               self.find_display.insert(tk.END, f"{item}\n")


       except Exception as e:
           logging.error(f"Error in search function: {str(e)}")


   def export_tree(self):
       try:
           tree_dict = self.trie.to_dict()
           with open('TreeDump.json', 'w', encoding='utf-8') as f:
               json.dump(tree_dict, f, ensure_ascii=False, indent=2)
       except Exception as e:
           logging.error(f"Error in export tree function: {str(e)}")
           raise


   def quit_app(self):
       try:
           self.root.quit()
           sys.exit(0)
       except Exception as e:
           logging.error(f"Error in quit function: {str(e)}")
           sys.exit(1)


def main():
   try:
       root = tk.Tk()
       app = SearchApp(root)
       root.mainloop()
   except Exception as e:
       logging.error(f"Error in main: {str(e)}")
       sys.exit(1)


if __name__ == "__main__":
   main()



