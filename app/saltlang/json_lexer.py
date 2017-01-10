from app.parser import lexer

RESERVED = 'RESERVED'
ID = "ID"
VALUE = "VALUE"
QUOTED = "QUOTED"
INT = "INT"
FLOAT = "FLOAT"
BOOL = "BOOL"
# an array of tuples, keep all token
token_exprs = [
    (r'[ \n\t]+',              None), # space  should be ignored
    (r'\'[^\']*\'',             QUOTED),
    (r'"[^"]*\"',               QUOTED),
    (r':',                    RESERVED),
    (r'\[',                    RESERVED),
    (r'\]',                    RESERVED),
    (r'{',                    RESERVED),
    (r'}',                    RESERVED),
    (r'true',                     BOOL),
    (r'false',                    BOOL),
    (r',',                     RESERVED),
    (r'[+-]?([0-9]*\.?[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)?', INT),
    (r'[+-]?([0-9]*\.?[0-9]+|[0-9]+\.[0-9]*)([eE][+-]?[0-9]+)?', FLOAT),
    (r'[A-Za-z][A-Za-z0-9_]*',       ID),

]


def json_lex(characters):
    return lexer.lex(characters, token_exprs)

if __name__ == "__main__":
    cmd = "-1.324 1 1.0e14 true false abc"
    tokens = json_lex(cmd)
    print(tokens)