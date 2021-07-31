class HtmlArgument:
    def __init__(self):
        self.name = ''
        self.value = ''

    def add_to_name(self, ch):
        self.name += ch

    def add_to_value(self, ch):
        self.value += ch
