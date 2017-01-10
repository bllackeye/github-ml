from app.parser import lexer

RESERVED = 'RESERVED'
ID = "ID"
STRING = "STRING"
WORD = "WORD"
# an array of tuples, keep all token
token_exprs = [
    (r'[ \n\t]+',              None), # space  should be ignored
    (r'\'[^\']*\'',             STRING),
    (r'"[^"]*\"',               STRING),
    (r'\.',                    RESERVED),
    (r'-G',                    RESERVED),
    (r'-E',                    RESERVED),
    (r'-L',                    RESERVED),
    (r'-C',                    RESERVED),
    #(r'-',                     RESERVED),
    (r'=',                     RESERVED),
    (r'salt-run',              RESERVED),
    (r'salt-key',              RESERVED),
    (r'salt',                  RESERVED),
    (r'[A-Za-z][A-Za-z0-9_]*',       ID),
    (r'[^\s]+',                      WORD)

]


def salt_lex(characters):
    return lexer.lex(characters, token_exprs)

if __name__ == "__main__":
    cmd = "salt '*' test.ping v1 v2 tag='[\"value1\",\"value2\"]'"
    tokens = salt_lex(cmd)
    print(tokens)