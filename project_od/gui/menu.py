class Menu:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.tot_page = 0
        self.__page = -1
        self.__panel = None
        self.__pages = {}
        self.__pages_id = {}
    
    def update(self):
        if self.__panel == None: 
            raise AttributeError("You need to put call page")
        self.__panel.update()
        self.__panel.draw(self.screen)
    
    def page(self, name=""):
        page_level = self.tot_page
        if name:
            self.__pages[name] = page_level
        self.tot_page += 1
        def wrappers(method):
            def _page(*args):
                if self.__page != page_level:
                    self.__page = page_level
                    ret = method(self, *args)
                    if ret != None:
                        self.__panel = ret
                return ret
            self.__pages_id[page_level] = _page
            return _page
        return wrappers
    
    def get_current_page(self):
        return self.__page
    
    def get_page_id(self, name : str):
        return self.__pages[name]
    
    def get_page(self, name : str|int):
        if isinstance(name, str):
            name = self.get_page_id(name)
        return self.__pages_id[name]
    
    def add_page(self, page, name=""):
        return self.page(name)(page)
    
    def __call__(self, name, *args) -> None:
        return self.get_page(name)(*args)