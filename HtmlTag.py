from HtmlArgument import HtmlArgument


class HtmlTag:
    def __init__(self):
        self.childTags = []
        self.rawBody = ''
        self.html = ''
        self.i = 0
        self.name = ''
        self.args = []
        self.close_name = None
        self.tags_without_ending = ['area', 'base', 'command', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen',
                                    'link', 'meta', 'param', 'source', 'track', 'wbr']

    def add_tag(self, tag):
        self.childTags.append(tag)

    def add_symbol(self, s):
        self.rawBody += s

    def write(self, html, start_index=0):
        self.html = html
        self.i = start_index
        while self.i < len(self.html):
            ch = self.html[self.i]
            if self.close_name is not None or ch == '>' and self.name in self.tags_without_ending:
                return self.i
            if ch == '<':
                self.inc()
                self.write_inner_tag()
                continue
            if ch == '>':
                self.inc()
                self.write_body()
                continue
            if ch == '/' and self.html[self.i + 1] == '>':
                return self.i + 1
            raise ValueError('Incorrect html')

    def write_inner_tag(self):
        self.write_name()
        while self.i < len(self.html):
            ch = self.html[self.i]
            if ch == ' ':
                self.inc()
                self.write_argument()
                continue
            if ch == '>' or ch == '/':
                break
            raise ValueError('Inner tag must end with > symbol')

    def write_name(self):
        while self.i < len(self.html):
            ch = self.html[self.i]
            if ch == ' ' or ch == '>' or ch == '/':
                break
            self.name += ch
            self.inc()

    def write_argument(self):
        arg = HtmlArgument()

        self.write_argument_name(arg)
        ch = self.cur()
        if len(arg.name) > 0:
            self.args.append(arg)
        if ch == ' ' or ch == '/' or ch == '>':
            arg.value = None
            return
        if ch != '=':
            raise ValueError('= expected in argument')

        self.inc()
        self.write_argument_value(arg)
        ch = self.cur()
        if ch != '"':
            raise ValueError('" expected in argument parameter ending')
        self.inc()
        ch = self.cur()
        if ch != '>' and ch != ' ' and ch != '/':
            raise ValueError('>,space or / expected after argument parameter ending')

    def write_argument_name(self, arg):
        while self.i < len(self.html):
            ch = self.cur()
            if ch == '=' or ch == ' ' or ch == '/' or ch == '>':
                break
            arg.add_to_name(ch)
            self.inc()

    def write_argument_value(self, arg):
        if self.cur() != '"':
            raise ValueError('" expected in argument parameter beginning')
        self.inc()
        while self.i < len(self.html):
            ch = self.cur()
            if ch == '"':
                break
            arg.add_to_value(ch)
            self.inc()

    def write_body(self):
        while self.i < len(self.html):
            ch = self.cur()
            if ch != '<':
                self.write_raw_text()
                continue
            if self.next() != '/':
                self.write_tag()
                self.inc()
                continue
            self.write_close_tag()
            if self.close_name != self.name:
                raise ValueError('Close tag must be equal open tag')
            break

    def write_tag(self):
        tag = HtmlTag()
        self.i = tag.write(self.html, self.i)
        self.childTags.append(tag)
        if self.cur() != '>':
            raise ValueError('> expected in inner tag ending')

    def write_close_tag(self):
        if self.cur() != '<' or self.next() != '/':
            raise ValueError('</ expected in close tag')
        self.close_name = ''
        self.inc()
        self.inc()
        while self.i < len(self.html):
            ch = self.cur()
            if ch == '>':
                break
            self.close_name += ch
            self.inc()

    def write_raw_text(self):
        while self.i < len(self.html):
            ch = self.cur()
            if ch == '<':
                # self.rawBody += '\n'
                break
            self.rawBody += ch
            self.inc()

    def inc(self):
        self.i += 1

    def cur(self):
        return self.html[self.i]

    def next(self):
        return self.html[self.i + 1]
