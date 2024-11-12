import os
import subprocess
from pycparser import c_parser, c_ast
from pycparser.plyparser import ParseError
from graphviz import Digraph
import pycparser

def preprocess_c_file(filename):
    """Pré-processa o código C usando o gcc e retorna o conteúdo pré-processado"""
    preprocessed_filename = filename.replace('.c', '_preprocessed.c')
    try:
        subprocess.run(['gcc', '-E', filename, '-o', preprocessed_filename], check=True)
        with open(preprocessed_filename, 'r') as file:
            code = file.read()
        os.remove(preprocessed_filename)
        return code
    except subprocess.CalledProcessError:
        print(f"Erro ao pré-processar o arquivo {filename}")
        return None

def parse_c_file(filename):
    """Faz o parse do código C usando pycparser"""
    code = preprocess_c_file(filename)
    if code is None:
        return None

    fake_include_path = os.path.join(os.path.dirname(pycparser.__file__), 'utils', 'fake_libc_include')
    
    parser = c_parser.CParser()
    try:
        ast = parser.parse(code, fake_libc_include=fake_include_path)
        return ast
    except ParseError as e:
        print(f"Erro ao fazer o parse do arquivo {filename}: {e}")
        return None

def create_cfg_for_function(func_ast, func_name):
    """Cria o grafo de fluxo de controle para uma função"""
    cfg = Digraph(name=func_name, format='png')
    cfg.attr(rankdir='TB')
    node_counter = 0

    def add_node(label):
        nonlocal node_counter
        node_id = f'node{node_counter}'
        cfg.node(node_id, label)
        node_counter += 1
        return node_id

    def traverse_ast(node):
        """Percorre o AST e adiciona nós ao CFG"""
        if isinstance(node, c_ast.FuncDef):
            entry_node = add_node(f"{func_name}: Entry")
            last_node = entry_node
            if node.body:
                last_node = traverse_ast(node.body)
            exit_node = add_node(f"{func_name}: Exit")
            cfg.edge(last_node, exit_node)
            return entry_node
        elif isinstance(node, c_ast.Compound):
            last_node = None
            for stmt in node.block_items:
                current_node = traverse_ast(stmt)
                if last_node:
                    cfg.edge(last_node, current_node)
                last_node = current_node
            return last_node
        elif isinstance(node, c_ast.If):
            if_node = add_node("If")
            true_node = traverse_ast(node.iftrue)
            false_node = traverse_ast(node.iffalse) if node.iffalse else None
            cfg.edge(if_node, true_node, label="True")
            if false_node:
                cfg.edge(if_node, false_node, label="False")
            return if_node
        elif isinstance(node, c_ast.While):
            while_node = add_node("While")
            body_node = traverse_ast(node.stmt)
            cfg.edge(while_node, body_node)
            cfg.edge(body_node, while_node)
            return while_node
        else:
            return add_node(type(node).__name__)

    traverse_ast(func_ast)
    return cfg

def generate_cfg_images(filename):
    """Gera CFGs para cada função no arquivo C"""
    ast = parse_c_file(filename)
    if ast is None:
        print(f"Erro ao processar o arquivo {filename}")
        return

    for ext in ast.ext:
        if isinstance(ext, c_ast.FuncDef):
            func_name = ext.decl.name
            cfg = create_cfg_for_function(ext, func_name)
            output_path = f"{os.path.splitext(os.path.basename(filename))[0]}_{func_name}.png"
            cfg.render(output_path, format='png')
            print(f"Grafo de fluxo de controle gerado para {func_name}: {output_path}")

def process_c_files_in_directory(root_dir):
    """Percorre recursivamente o diretório raiz e processa todos os arquivos .c"""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.c'):
                c_file_path = os.path.join(dirpath, filename)
                generate_cfg_images(c_file_path)

# Exemplo de execução
process_c_files_in_directory('src')
