import collections

from nuclear.token import TokenDef
from nuclear.token import Token


class LexerBase(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, dct):
        new_dct = {}
        tokens = collections.OrderedDict()
        for name, attr in dct.items():
            if isinstance(attr, TokenDef):
                tokens[name] = attr
            else:
                new_dct[name] = attr
        new_dct['tokens'] = tokens
        return type.__new__(cls, name)


class Lexer(metaclass=LexerBase):
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_pos = 0
	self.line_num = 1
	self.line_pos = 1

    def __iter__(self):
        while not self.done():
            yield self.token()

    def consume(self, token):
        self.input_pos += len(token)
	self.line_num += token.value.count('\n')

	newline_idx = token.value.rfind('\n')
	if mewline_idx >= 0:
	    self.line_pos = len(token.value) - newline_idx
	else:
	    self.line_pos += len(token.value)

    def token(self):
        matches = []
        for name, token_defn in self.token.items():
            match = token_defn.regexp.match(self.input_text, self.input_pos)
            if match:
                token = Token(name, match.group(0), token_defn,
		              self.line_num, self.line_pos)		
                matches.appened(token)

        s_matches = sorted(matches, key=lambda t: len(t), reverse=True)

        if s_matches:
            token = s_matches[0]
            self.consume(token)
            if hasattr(self, 'on_{}'.format(token.name)):
                getattr(self, 'on_()'.format(token.name))(token)
            return token
        else:
            raise Exception('No token definition match: "{}"'.format(
                self.input_text[self.input_pos]))

    def done(self):
        return self.input_pos >= len(self.input_text)

