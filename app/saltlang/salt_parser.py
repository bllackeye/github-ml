from app.parser.parser_combinator import *
from app.saltlang.salt_lexer import *
from app.saltlang.salt_AST import *
from app.saltlang.json_parser import *
import logging

import logging.config

logger = logging.getLogger(__name__)


def keyword(kw):
    return Reserved(kw, RESERVED)

quoted_value = Tag(STRING)


def quoted():
    def process(parsed):
        text = parsed[1:][:-1]
        try:
            return json_parse(text)
        except Exception as error:
            return text

    return quoted_value ^ process


def singlecmd():
    def process(parsed):
        (cl, fun) = parsed
        (f, plist) = fun
        cl.setfun(f)
        cl.setparams(plist)
        return cl
    return client() + function() ^ process


def client():
    return master_cmd() | minion_cmd()


def runner():
    return keyword("salt-run")


def wheel():
    return keyword("salt-key")


def minion_cmd():
    def process(parsed):
        (cl, (opt, tgt)) = parsed
        return MinionCmd(cl, opt, tgt)
    return (minion() + target()) ^ process


def master_cmd():
    def process(parsed):
        return MasterCmd(parsed)

    return (runner() | wheel()) ^ process


def minion():
    return keyword("salt")


def target_option():
    return Opt(keyword("-C")) | keyword("-G") | keyword("-L") | keyword("-E")


def target():
    return target_option() + quoted()


def module():
    connector = keyword(".") ^ (lambda x: lambda l, r: PathPart(l, r))
    return Exp(Tag(ID), connector)


def free_form_value():
    return Tag(WORD) | Tag(ID)


def dot_value():
    return keyword('.')+free_form_value()


def dot_connected():
    def process(parsed):
        return parsed
    connector = keyword(".") ^ (lambda x: lambda l, r: PathPart(l, r))
    return Exp(free_form_value(), connector ) ^ process


def function():
    def process(parsed):
        return parsed
    return (module() + Opt(param_list())) ^ process


def value():
    return quoted() | free_form_value()


def arg():
    def process(parsed):
        return Param(None, parsed)
    return (dot_connected() | value()) ^ process


def param():
    return kwarg() | arg()


def param_list():
    return Rep(param())


def kwarg():
    def process(parsed):
        ((name, _), _val) = parsed
        return Param(name, _val)
    return (Tag(ID)+keyword('=')+value()) ^ process


def parser():
    return Phrase(singlecmd())


def salt_parse(text):
    tks = salt_lex(text)
    logger.info(tks)
    result = parser()(tks, 0)
    js = result.value.tojson()
    logger.info(js)
    return js


if __name__ == "__main__":
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,  # this fixes the problem
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': {
                '': {
                        'handlers': ['default'],
                        'level': 'INFO',
                        'propagate': True
                    }
            }
        }
    )
    logger.info('It works!')
    #cmd = "salt  '*' test.mypac.ping 'a'  b c fdafda03343&&&----241243 var='hhc'"
    #cmd = "salt  '*' test.mypac.ping abc.def.hh a var=hhc"
    #cmd = "salt-run manage.down removekeys=True"
    #cmd = "salt '*' test.arg 1 \"two\" 3.1 txt=\"hello\" wow='{a: 1, b: \"hello\"}'"
    #cmd=" salt '*' test.cross_test file.gid_to_group 0 "
    cmd = "salt-key test.mypack.ping v1 v2 tag='[\"value1\",\"value2\"]'"
    ast = salt_parse(cmd)
    logger.info("================ast=======================")
    logger.info(ast)
