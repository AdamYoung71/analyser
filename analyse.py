import graphviz
import argparse
from pycparser import parse_file
from pycparser import c_generator, c_ast


class UnsupportedLanguageConstruct(Exception):
    pass


class ExpressionVisitor:

    def __init__(self):
        self.variables = {}

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        raise UnsupportedLanguageConstruct(node.__class__.__name__)

    def visit_Constant(self, n):
        return n.value

    def visit_ID(self, n):
        return n.name

    def visit_UnaryOp(self, n):
        return n.op
        return n.expr

    def visit_BinaryOp(self, n):
        return n.op
        return n.left
        return n.right
    

class StatementVisitor:

    def __init__(self):
        self._c_generator = c_generator.CGenerator()
        self._availabe_label_index = 0
        self._cfg = graphviz.Digraph('control_flow_graph', filename='cfg.gv')
        self._cfg.attr('node', shape='box')

    def _new_label(self):
        id = "l" + str(self._availabe_label_index)
        self._availabe_label_index += 1
        return id

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        raise UnsupportedLanguageConstruct(node.__class__.__name__)

    def visit_FileAST(self, n):
        for ext in n.ext:
            if isinstance(ext, c_ast.FuncDef):
                self.visit(ext)
            else:
                raise UnsupportedLanguageConstruct(node.__class__.__name__)

    def visit_FuncDef(self, n):
        assert(n.decl.name == 'main')
        self.visit(n.body)

    def visit_Compound(self, n):
        for stmt in n.block_items:
            self.visit(stmt)

    def visit_If(self, n):
        if n.cond is None:
            return

        cond_label = self._new_label()
        self._cfg.node(cond_label,
                       label=self._c_generator.visit(n.cond),
                       xlabel=cond_label)
        expr_visitor = ExpressionVisitor()
        expr_visitor.visit(n.cond)

        if n.iftrue is not None:
            iftrue_label = self._new_label()
            self._cfg.node(iftrue_label,
                           label=self._c_generator.visit(n.iftrue),
                           xlabel=iftrue_label)
            self._cfg.edge(cond_label, iftrue_label, label='true')
            self.visit(n.iftrue)

        if n.iffalse is not None:
            iffalse_label = self._new_label()
            self._cfg.node(iffalse_label,
                           label=self._c_generator.visit(n.iffalse),
                           xlabel=iffalse_label)
            self._cfg.edge(cond_label, iffalse_label, label='false')
            self.visit(n.iffalse)

    def visit_FuncCall(self, n):
        name = n.name
        for arg in n.args:
            expr_visitor = ExpressionVisitor()
            expr_visitor.visit(arg)

    def visit_While(self, n):
        if n.cond is None:
            return

        expr_visitor = ExpressionVisitor()
        expr_visitor.visit(n.cond)

        if n.stmt is not None:
            self.visit(n.stmt)

    def visit_Assignment(self, n):
        expr_visitor = ExpressionVisitor()
        expr_visitor.visit(n.rvalue)
        expr_visitor = ExpressionVisitor()
        expr_visitor.visit(n.lvalue)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='COMP0174 Analyser.')
    parser.add_argument('file', metavar='FILE', help='a file for analysing (- for using stdin)')
    args = parser.parse_args()
    ast = parse_file(args.file)
    v = StatementVisitor()
    v.visit(ast)
    v._cfg.render(directory='doctest-output')
