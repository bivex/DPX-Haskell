# Generated from src/pattern_detector/adapters/outbound/parsers/antlr/grammars/Haskell.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .HaskellParser import HaskellParser
else:
    from HaskellParser import HaskellParser

# This class defines a complete generic visitor for a parse tree produced by HaskellParser.

class HaskellVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HaskellParser#haskellModule.
    def visitHaskellModule(self, ctx:HaskellParser.HaskellModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#moduleHeader.
    def visitModuleHeader(self, ctx:HaskellParser.ModuleHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#modId.
    def visitModId(self, ctx:HaskellParser.ModIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#exports.
    def visitExports(self, ctx:HaskellParser.ExportsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#exportItem.
    def visitExportItem(self, ctx:HaskellParser.ExportItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#exportSubItem.
    def visitExportSubItem(self, ctx:HaskellParser.ExportSubItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#pragma.
    def visitPragma(self, ctx:HaskellParser.PragmaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#topDeclaration.
    def visitTopDeclaration(self, ctx:HaskellParser.TopDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#importDeclaration.
    def visitImportDeclaration(self, ctx:HaskellParser.ImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#importList.
    def visitImportList(self, ctx:HaskellParser.ImportListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#importItem.
    def visitImportItem(self, ctx:HaskellParser.ImportItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#dataDeclaration.
    def visitDataDeclaration(self, ctx:HaskellParser.DataDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#newtypeDeclaration.
    def visitNewtypeDeclaration(self, ctx:HaskellParser.NewtypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeSynonymDeclaration.
    def visitTypeSynonymDeclaration(self, ctx:HaskellParser.TypeSynonymDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeFamilyDeclaration.
    def visitTypeFamilyDeclaration(self, ctx:HaskellParser.TypeFamilyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeFamilyInstances.
    def visitTypeFamilyInstances(self, ctx:HaskellParser.TypeFamilyInstancesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeFamilyInstance.
    def visitTypeFamilyInstance(self, ctx:HaskellParser.TypeFamilyInstanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#simpleType.
    def visitSimpleType(self, ctx:HaskellParser.SimpleTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeVar.
    def visitTypeVar(self, ctx:HaskellParser.TypeVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#constructors.
    def visitConstructors(self, ctx:HaskellParser.ConstructorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#constructor.
    def visitConstructor(self, ctx:HaskellParser.ConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#fieldDecl.
    def visitFieldDecl(self, ctx:HaskellParser.FieldDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#recordField.
    def visitRecordField(self, ctx:HaskellParser.RecordFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#gadtConstructors.
    def visitGadtConstructors(self, ctx:HaskellParser.GadtConstructorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#gadtConstructor.
    def visitGadtConstructor(self, ctx:HaskellParser.GadtConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#derivingClause.
    def visitDerivingClause(self, ctx:HaskellParser.DerivingClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#derivingStrategy.
    def visitDerivingStrategy(self, ctx:HaskellParser.DerivingStrategyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#derivingTarget.
    def visitDerivingTarget(self, ctx:HaskellParser.DerivingTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#standaloneDeriving.
    def visitStandaloneDeriving(self, ctx:HaskellParser.StandaloneDerivingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeClassDeclaration.
    def visitTypeClassDeclaration(self, ctx:HaskellParser.TypeClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#classBody.
    def visitClassBody(self, ctx:HaskellParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#classMember.
    def visitClassMember(self, ctx:HaskellParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#instanceDeclaration.
    def visitInstanceDeclaration(self, ctx:HaskellParser.InstanceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#instanceBody.
    def visitInstanceBody(self, ctx:HaskellParser.InstanceBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#instanceMember.
    def visitInstanceMember(self, ctx:HaskellParser.InstanceMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#context.
    def visitContext(self, ctx:HaskellParser.ContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#classConstraint.
    def visitClassConstraint(self, ctx:HaskellParser.ClassConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#functionSignature.
    def visitFunctionSignature(self, ctx:HaskellParser.FunctionSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#varIdList.
    def visitVarIdList(self, ctx:HaskellParser.VarIdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#functionBinding.
    def visitFunctionBinding(self, ctx:HaskellParser.FunctionBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#guards.
    def visitGuards(self, ctx:HaskellParser.GuardsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#guardExpr.
    def visitGuardExpr(self, ctx:HaskellParser.GuardExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#localDeclarations.
    def visitLocalDeclarations(self, ctx:HaskellParser.LocalDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#localDeclaration.
    def visitLocalDeclaration(self, ctx:HaskellParser.LocalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#fixityDeclaration.
    def visitFixityDeclaration(self, ctx:HaskellParser.FixityDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#defaultDeclaration.
    def visitDefaultDeclaration(self, ctx:HaskellParser.DefaultDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#typeExpr.
    def visitTypeExpr(self, ctx:HaskellParser.TypeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#btype.
    def visitBtype(self, ctx:HaskellParser.BtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#atype.
    def visitAtype(self, ctx:HaskellParser.AtypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#kind.
    def visitKind(self, ctx:HaskellParser.KindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#pattern.
    def visitPattern(self, ctx:HaskellParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#apat.
    def visitApat(self, ctx:HaskellParser.ApatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#fieldPattern.
    def visitFieldPattern(self, ctx:HaskellParser.FieldPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#expr.
    def visitExpr(self, ctx:HaskellParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#infixExpr.
    def visitInfixExpr(self, ctx:HaskellParser.InfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#prefixExpr.
    def visitPrefixExpr(self, ctx:HaskellParser.PrefixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:HaskellParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#listCompQuals.
    def visitListCompQuals(self, ctx:HaskellParser.ListCompQualsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#listCompQual.
    def visitListCompQual(self, ctx:HaskellParser.ListCompQualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#doBlock.
    def visitDoBlock(self, ctx:HaskellParser.DoBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#doStatement.
    def visitDoStatement(self, ctx:HaskellParser.DoStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#caseAlternatives.
    def visitCaseAlternatives(self, ctx:HaskellParser.CaseAlternativesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#caseAlternative.
    def visitCaseAlternative(self, ctx:HaskellParser.CaseAlternativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#fieldUpdate.
    def visitFieldUpdate(self, ctx:HaskellParser.FieldUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#op.
    def visitOp(self, ctx:HaskellParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#qvar.
    def visitQvar(self, ctx:HaskellParser.QvarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#qcon.
    def visitQcon(self, ctx:HaskellParser.QconContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by HaskellParser#literal.
    def visitLiteral(self, ctx:HaskellParser.LiteralContext):
        return self.visitChildren(ctx)



del HaskellParser