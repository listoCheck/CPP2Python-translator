from lexer import lexer
from parser import Parser
from codegen import generate


def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        code = f.read()
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    python_code = generate(ast)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(python_code)


if __name__ == "__main__":
    main()
