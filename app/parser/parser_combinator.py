class Result(object):
    def __init__(self, value, pos):
        self.value = value  # typically is a AST node, this is how AST and parser combinator connected.
        self.pos = pos

    def __repr__(self):
        return 'Result(%s, %d)' % (self.value, self.pos)


'''
The other methods, __add__, __mul__, __or__, and __xor__ define the +, *, |, and ^ operators, respectively.
Each operator provides a shortcut for calling a different combinator. We'll cover each of these combinators shortly.
'''


class Parser(object):
    def __call__(self, tokens, pos):
        return None  # subclasses will override this

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)

'''
Reserved will be used to parse reserved words and operators; it will accept tokens with a specific value and tag.
Remember, tokens are just value-tag pairs. token[0] is the value, token[1] is the tag.
'''


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and \
           tokens[pos][0] == self.value and \
           tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None

'''
Moving on, the Tag combinator is very similar to Reserved. It matches any token which has a particular tag.
The value can be anything. It is used to indicate the token is a instance of certain type, saying a number.
'''


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None


'''
The Tag and Reserved combinators are our primitives. All combinators will be built out of them at the most basic level.
The Concat combinator will take two parsers as input (left and right). When applied, a Concat parser will apply
the left parser, followed by the right parser. If both are successful, the result value will be a pair containing the
left and right results. If either parser is unsuccessful, None is returned.
'''


class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            right_result = self.right(tokens, left_result.pos)
            if right_result:
                combined_value = (left_result.value, right_result.value)
                return Result(combined_value, right_result.pos)
        return None
'''
The Alternate combinator is similar. It also takes left and right parsers. It starts by applying the left parser.
If successful, that result is returned. If unsuccessful, it applies the right parser and returns its result.
Alternate is useful for choosing among several possible parsers.

'''


class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left_result = self.left(tokens, pos)
        if left_result:
            return left_result
        else:
            right_result = self.right(tokens, pos)
            return right_result

'''
Opt is useful for optional text, such as the else-clause of an if-statement. It takes one parser as input.
 If that parser is successful when applied, the result is returned normally. If it fails, a successful result is still
  returned, but the value of that result is None. No tokens are consumed in the failure case; the result position
  is the same as the input position.
'''


class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return Result(None, pos)

'''
Rep applies its input parser repeatedly until it fails. This is useful for generating lists of things. Note that Rep
will successfully match an empty list and consume no tokens if its parser fails the first time it's applied.
'''


class Rep(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)

'''
Process is a useful combinator which allows us to manipulate result values. Its input is a parser and a function.
 When the parser is applied successfully, the result value is passed to the function, and the return value from
 the function is returned instead of the original value. We will use Process to actually build the AST nodes out of
the pairs and lists that Concat and Rep return.
'''


class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result

'''
Lazy is a less obviously useful combinator. Instead of taking an input parser, it takes a zero-argument function which
 returns a parser. Lazy will not call the function to get the parser until it's applied. This is needed to build
 recursive parsers (like how arithmetic expressions can include arithmetic expressions). Since such a parser refers
 to itself, we can't just define it by referencing it directly; at the time the parser's defining expression is
 evaluated, the parser is not defined yet. We would not need this in a language with lazy evaluation like Haskell
 or Scala, but Python is anything but lazy.
'''


class Lazy(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        # typically, calling parser_func will return a parsers which contains
        # a new Lazy(something) parser.
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)


'''
 Phrase, takes a single input parser, applies it, and returns its result normally. The only catch is that it will fail
  if its input parser did not consume all of the remaining tokens. The top level parser for IMP will be a Phrase parser.
   This prevents us from partially matching a program which has garbage at the end.
'''


class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else:
            return None

'''
 Exp takes two parsers as input. The first parser matches the actual elements of the list. The second matches the
 separators. On success, the connector parser must return a function which combines elements parsed on the left and
 right into a single value. This value is accumulated for the whole list, left to right, and is ultimately returned.


 handle the scenario like :  Parser [connector Parser]+
 connector itself is parser expecting a seperator but return a function taking 2 parameter,which knows how to
 do composition.

 An example for connector: connector = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
'''


class Exp(Parser):
    # seperator is function, return a parser on invoke.
    def __init__(self, parser, connector):
        self.parser = parser
        self.connector = connector

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        # this is to invoke Process

        def process_next(parsed):
            (sepfunc, right) = parsed
            # sepfunc knows how to combine result.value and a parser right.
            return sepfunc(result.value, right)

        # self.separator + self.parser is a parser itself with Result, the value part
        # is two results keep in tuple
        # ((left_result,right_result), position)

        # next_parser is a processor.

        next_parser = self.connector + self.parser ^ process_next

        # next_parser= Process(Concat(self.seperator, self.parser), process_next)
        # next_parser(tokens,result.pos)
        # Concat(self.seperator,self.parser) invokes self.seperator first, and then self.parser

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result