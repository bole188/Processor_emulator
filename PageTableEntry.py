import collections

class PageTableLevel:
    def __init__(self, level):
        self.level = level
        self.entries = [None] * 512 


root_page_table = PageTableLevel(4)  
