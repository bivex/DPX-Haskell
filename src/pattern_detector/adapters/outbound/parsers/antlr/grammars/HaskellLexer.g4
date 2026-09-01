lexer grammar HaskellLexer;

// Pragmas
PRAGMA_START : '{-#' -> pushMode(PRAGMA_MODE);
BLOCK_COMMENT : '{-' (BLOCK_COMMENT | .)*? '-}' -> channel(HIDDEN);
LINE_COMMENT  : '--' ~[\r\n]* -> channel(HIDDEN);

// Keywords
MODULE      : 'module';
WHERE       : 'where';
IMPORT      : 'import';
QUALIFIED   : 'qualified';
AS          : 'as';
HIDING      : 'hiding';
DATA        : 'data';
NEWTYPE     : 'newtype';
TYPE        : 'type';
FAMILY      : 'family';
CLASS       : 'class';
INSTANCE    : 'instance';
DERIVING    : 'deriving';
STOCK       : 'stock';
ANYCLASS    : 'anyclass';
DEFAULT     : 'default';
FORALL      : 'forall';
DO          : 'do';
MDO         : 'mdo';
CASE        : 'case';
OF          : 'of';
IF          : 'if';
THEN        : 'then';
ELSE        : 'else';
LET         : 'let';
IN          : 'in';

// Symbols & Punctuation
DCOLON      : '::';
ARROW       : '->';
LARROW      : '<-';
DARROW      : '=>';
PIPE        : '|';
EQUAL       : '=';
SEMI        : ';';
COMMA       : ',';
DOT         : '.';
BACKSLASH   : '\\';
TILDE       : '~';
AT          : '@';
LPAREN      : '(';
RPAREN      : ')';
LBRACK      : '[';
RBRACK      : ']';
LBRACE      : '{';
RBRACE      : '}';
BACKTICK    : '`';
TICK        : '\'';

// Operators (symbols)
OPERATOR    : [!#$%&*+./<=>?@\\^|~:-]+;

// Identifiers
CONID       : [A-Z][a-zA-Z0-9_']* ;
VARID       : [a-z_][a-zA-Z0-9_']* ;

// Literals
INTEGER     : [0-9]+ ;
FLOAT       : [0-9]+ '.' [0-9]+ ([eE] [+-]? [0-9]+)? ;
CHAR_LIT    : '\'' ( ~['\\] | '\\' . ) '\'' ;
STRING_LIT  : '"' ( ~["\\] | '\\' . )*? '"' ;

// Whitespace
WS          : [ \t\r\n]+ -> channel(HIDDEN);

mode PRAGMA_MODE;
LANGUAGE_KW : 'LANGUAGE' ;
OPTIONS_GHC : 'OPTIONS_GHC' ;
PRAGMA_END  : '#-}' -> popMode;
PRAGMA_TEXT : ~[\r\n#]+ ;
PRAGMA_WS   : [ \t\r\n]+ -> channel(HIDDEN);
