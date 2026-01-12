from ast_nodes import *


def generate(node, indent=0):
    pad = '    ' * indent
    if isinstance(node, Program):
        return '\n'.join(generate(s) for s in node.statements)
    if isinstance(node, Class):
        body = '\n'.join(generate(m, indent + 1) for m in node.members)
        return f"{pad}class {node.name}:\n{body or pad + '    pass'}"
    if isinstance(node, Func):
        params = ', '.join(node.params)
        body = '\n'.join(generate(s, indent + 1) for s in node.body)
        return f"{pad}def {node.name}({params}):\n{body or pad + '    pass'}"
    if isinstance(node, Assign):
        return f"{pad}{node.name} = {generate(node.expr) if node.expr else '0'}"
    if isinstance(node, If):
        body = '\n'.join(generate(s, indent + 1) for s in node.body)
        return f"{pad}if {generate(node.cond)}:\n{body or pad + '    pass'}"
    if isinstance(node, While):
        body = '\n'.join(generate(s, indent + 1) for s in node.body)
        return f"{pad}while {generate(node.cond)}:\n{body or pad + '    pass'}"
    if isinstance(node, BinOp):
        return f"{generate(node.left)} {node.op} {generate(node.right)}"
    if isinstance(node, Number):
        return node.value
    if isinstance(node, Variable):
        return node.name
    if isinstance(node, FuncCall):
        args = ', '.join(generate(a) for a in node.args)
        return f"{node.name}({args})"
    if isinstance(node, Return):
        return f"{pad}return {generate(node.expr)}"
    if isinstance(node, Cin):
        return '\n'.join(f"{pad}{v} = int(input())" for v in node.vars)
    if isinstance(node, Cout):
        return '\n'.join(f"{pad}print({generate(e)})" for e in node.outputs)
    if isinstance(node, Comment):
        comment_text = node.text
        if comment_text.startswith('//'):
            return f"{pad}# {comment_text[2:].strip()}"
        elif comment_text.startswith('/*') and comment_text.endswith('*/'):
            lines = comment_text[2:-2].splitlines()
            return '\n'.join(f"{pad}# {line.strip()}" for line in lines)
