parser grammar HaskellParser;

options { tokenVocab=HaskellLexer; }

// Top-level module
haskellModule
    : pragma* (moduleHeader)? (topDeclaration | pragma)* EOF
    ;

moduleHeader
    : MODULE modId (exports)? WHERE
    ;

modId
    : CONID (DOT CONID)*
    ;

exports
    : LPAREN (exportItem (COMMA exportItem)*)? (COMMA)? RPAREN
    ;

exportItem
    : qvar
    | qcon (LPAREN (DOT DOT | (exportSubItem (COMMA exportSubItem)*)?) RPAREN)?
    | MODULE modId
    ;

exportSubItem
    : qvar
    | qcon
    ;

pragma
    : PRAGMA_START pragmaBody PRAGMA_END
    ;

pragmaBody
    : LANGUAGE_KW CONID (COMMA CONID)*
    | OPTIONS_GHC pragmaString*
    | pragmaString*
    ;

pragmaString
    : CONID | VARID | OPERATOR | INTEGER | STRING_LIT | PRAGMA_TEXT
    ;

topDeclaration
    : importDeclaration
    | dataDeclaration
    | newtypeDeclaration
    | typeSynonymDeclaration
    | typeFamilyDeclaration
    | typeClassDeclaration
    | instanceDeclaration
    | functionSignature
    | functionBinding
    | fixityDeclaration
    | standaloneDeriving
    | defaultDeclaration
    ;

importDeclaration
    : IMPORT (QUALIFIED)? modId (AS modId)? (HIDING)? (importList)?
    ;

importList
    : LPAREN (importItem (COMMA importItem)*)? (COMMA)? RPAREN
    ;

importItem
    : qvar
    | qcon (LPAREN (DOT DOT | (qvar (COMMA qvar)*)?) RPAREN)?
    ;

// Data declaration (Standard or GADT)
dataDeclaration
    : DATA (FAMILY)? simpleType (EQUAL constructors)? (WHERE gadtConstructors)? (derivingClause)*
    ;

newtypeDeclaration
    : NEWTYPE simpleType EQUAL constructor (derivingClause)*
    ;

typeSynonymDeclaration
    : TYPE simpleType EQUAL typeExpr
    ;

typeFamilyDeclaration
    : TYPE FAMILY simpleType (DCOLON kind)? (WHERE typeFamilyInstances)?
    ;

typeFamilyInstances
    : typeFamilyInstance*
    ;

typeFamilyInstance
    : TYPE typeExpr EQUAL typeExpr
    ;

simpleType
    : CONID (typeVar)*
    ;

typeVar
    : VARID
    | LPAREN typeVar (COMMA typeVar)* RPAREN
    ;

constructors
    : constructor (PIPE constructor)*
    ;

constructor
    : CONID (fieldDecl | atype)*
    | CONID LBRACE (recordField (COMMA recordField)*)? RBRACE
    ;

fieldDecl
    : atype
    ;

recordField
    : VARID (COMMA VARID)* DCOLON typeExpr
    ;

gadtConstructors
    : (gadtConstructor (SEMI)?)*
    ;

gadtConstructor
    : CONID DCOLON (context DARROW)? typeExpr
    ;

derivingClause
    : DERIVING (derivingStrategy)? (derivingTarget | LPAREN (derivingTarget (COMMA derivingTarget)*)? RPAREN)
    ;

derivingStrategy
    : STOCK
    | NEWTYPE
    | ANYCLASS
    ;

derivingTarget
    : CONID (typeVar)*
    ;

standaloneDeriving
    : DERIVING (derivingStrategy)? INSTANCE (context DARROW)? classConstraint
    ;

// Typeclasses
typeClassDeclaration
    : CLASS (context DARROW)? CONID (typeVar)* (WHERE classBody)?
    ;

classBody
    : (classMember (SEMI)?)*
    ;

classMember
    : functionSignature
    | typeFamilyDeclaration
    | functionBinding
    ;

instanceDeclaration
    : INSTANCE (context DARROW)? CONID (atype)* (WHERE instanceBody)?
    ;

instanceBody
    : (instanceMember (SEMI)?)*
    ;

instanceMember
    : functionBinding
    | functionSignature
    | typeSynonymDeclaration
    ;

context
    : classConstraint
    | LPAREN (classConstraint (COMMA classConstraint)*)? RPAREN
    ;

classConstraint
    : CONID (atype)*
    ;

// Functions
functionSignature
    : varIdList DCOLON (context DARROW)? typeExpr
    ;

varIdList
    : qvar (COMMA qvar)*
    ;

functionBinding
    : qvar pattern* (guards | EQUAL expr) (WHERE localDeclarations)?
    ;

guards
    : (PIPE guardExpr EQUAL expr)+
    ;

guardExpr
    : expr
    ;

localDeclarations
    : (localDeclaration (SEMI)?)*
    ;

localDeclaration
    : functionSignature
    | functionBinding
    | pattern EQUAL expr
    ;

fixityDeclaration
    : (VARID | OPERATOR) INTEGER? (qvar | OPERATOR) (COMMA (qvar | OPERATOR))*
    ;

defaultDeclaration
    : DEFAULT LPAREN (typeExpr (COMMA typeExpr)*)? RPAREN
    ;

// Types
typeExpr
    : (FORALL (typeVar)+ DOT)? btype (ARROW typeExpr)*
    ;

btype
    : atype+
    ;

atype
    : qcon
    | qvar
    | LPAREN (typeExpr (COMMA typeExpr)*)? RPAREN
    | LBRACK typeExpr RBRACK
    | TILDE atype
    | TICK CONID
    | INTEGER
    | STRING_LIT
    ;

kind
    : typeExpr
    ;

// Patterns
pattern
    : apat (OPERATOR apat)*
    ;

apat
    : qvar
    | qcon
    | literal
    | LPAREN (pattern (COMMA pattern)*)? RPAREN
    | LBRACK (pattern (COMMA pattern)*)? RBRACK
    | TILDE apat
    | BACKSLASH pattern+ ARROW expr
    | qcon LBRACE (fieldPattern (COMMA fieldPattern)*)? RBRACE
    ;

fieldPattern
    : qvar (EQUAL pattern)?
    | DOT DOT
    ;

// Expressions
expr
    : infixExpr (DCOLON (context DARROW)? typeExpr)?
    ;

infixExpr
    : prefixExpr (op prefixExpr)*
    ;

prefixExpr
    : primaryExpr+
    ;

primaryExpr
    : qvar
    | qcon
    | literal
    | LPAREN (expr (COMMA expr)*)? RPAREN
    | LBRACK (expr (COMMA expr)* | expr PIPE listCompQuals)? RBRACK
    | DO doBlock
    | MDO doBlock
    | IF expr THEN expr ELSE expr
    | CASE expr OF caseAlternatives
    | LET localDeclarations IN expr
    | BACKSLASH pattern+ ARROW expr
    | primaryExpr LBRACE (fieldUpdate (COMMA fieldUpdate)*)? RBRACE
    ;

listCompQuals
    : listCompQual (COMMA listCompQual)*
    ;

listCompQual
    : pattern LARROW expr
    | LET localDeclarations
    | expr
    ;

doBlock
    : (doStatement (SEMI)?)*
    ;

doStatement
    : LET localDeclarations
    | pattern LARROW expr
    | expr
    ;

caseAlternatives
    : (caseAlternative (SEMI)?)*
    ;

caseAlternative
    : pattern (guards | ARROW expr) (WHERE localDeclarations)?
    ;

fieldUpdate
    : qvar EQUAL expr
    | DOT DOT
    ;

op
    : OPERATOR
    | BACKTICK qvar BACKTICK
    | BACKTICK qcon BACKTICK
    ;

qvar
    : (CONID DOT)* VARID
    | LPAREN OPERATOR RPAREN
    ;

qcon
    : (CONID DOT)* CONID
    | LPAREN OPERATOR RPAREN
    ;

literal
    : INTEGER
    | FLOAT
    | CHAR_LIT
    | STRING_LIT
    ;
