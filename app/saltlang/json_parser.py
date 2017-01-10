from app.parser.parser_combinator import *
from app.saltlang.json_lexer import *
from app.saltlang.json_AST import *
import logging

logger = logging.getLogger(__name__)


def quoted():
    def process(parsed):
        return parsed[1:][:-1]
    return Tag(QUOTED) ^ process


def int_value():
    def process(parsed):
        return int(parsed)
    return Tag(INT) ^ process


def float_value():
    def process(parsed):
        return float(parsed)
    return Tag(FLOAT) ^ process


def bool_value():
    def process(parsed):
        if parsed == 'true':
            return True
        else:
            return False
    return Tag(BOOL) ^ process


value = int_value() | float_value() | bool_value() | quoted()


def val():
    def process(parsed):
        return parsed
    return (value | map_val() | list_val()) ^ process


def map_val():
    def process(parsed):
        ((_, js_), _) = parsed
        return js_
    return keyword("{")+Lazy(attr_list)+keyword("}") ^ process


def list_val():
    def process(parsed):
        ((_, l), _) = parsed
        return l
    return keyword("[")+Lazy(value_list)+keyword("]") ^ process


def attr_map():
    def process(parsed):
        ((_, js_), _) = parsed
        return js_
    return keyword("{") + attr_list() + keyword("}") ^ process


def following_attr():
    def process(parsed):
        (_, attribute) = parsed
        return attribute
    return keyword(",")+attr() ^ process


def following_value():
    def process(parsed):
        (_, v) = parsed
        return v
    return keyword(",")+val() ^ process


def value_list():
    def process(parsed):
        (first, rest) = parsed
        array = list()
        array.append(first)
        for i in rest:
            array.append(i)
        return array

    return val()+Rep(following_value()) ^ process


def attr_list():
    def process(parsed):
        (first, rest) = parsed
        json = {}
        first.set_attr(json)
        for i in rest:
            i.set_attr(json)
        return json
    return attr()+Rep(following_attr()) ^ process


def attr():
    def process(parsed):
        ((name, _), _value) = parsed
        return Attr(name, _value)
    return Tag(ID) + keyword(":") + val() ^ process


def jsn():
    return list_val() | map_val()


def keyword(kw):
    return Reserved(kw, RESERVED)


def parser():
    return Phrase(jsn())


def json_parse(text):
    tks = json_lex(text)
    logger.info(tks)
    result = parser()(tks, 0)
    return result.value


if __name__ == "__main__":
    js = "{a:1, b:2, c:'abc',d:1, e:{k:1,q:2}, l:['a','b',{c:1,c:2}]}"
    #js = "*\n"
    ast = json_parse(js)
    print("==============ast==================")
    print(ast)
