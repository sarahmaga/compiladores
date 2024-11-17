import os
import subprocess
import sys
import glob

def generate_cfgs_for_optimization_levels(source_file, target):
    print('source_file ',source_file)
    output_dir = os.path.join(target, os.path.basename(source_file))

    print(output_dir)
    """Gera CFGs para os níveis de otimização O1, O2 e O3."""
    output_dir = output_dir.replace('.c', '', 1)
    os.makedirs(output_dir, exist_ok=True)
    optimization_levels = ["O1", "O2", "O3"]

    for opt_level in optimization_levels:
        # Gerar bytecode LLVM com o nível de otimização especificado
        llvm_file = f"{output_dir}/{os.path.basename(source_file)}_{opt_level}.bc"
        print('llvm_file',llvm_file)
        try:
            subprocess.run(["clang", f"-{opt_level}", "-emit-llvm", "-c", source_file, "-o", llvm_file], check=True)
            print("clang "+ f"-{opt_level}"+ " -emit-llvm "+ "-c "+ source_file+"-o "+ llvm_file)
            print(f"Bytecode LLVM gerado: {llvm_file}")
        except subprocess.CalledProcessError:
            print(f"Erro ao gerar bytecode para o nível {opt_level}")
            continue
        
        # Gerar os arquivos .dot representando o CFG para cada função
        try:
            print(f"Gerando CFG para {llvm_file}")
            subprocess.run(["opt", "-dot-cfg", llvm_file, "-o", "/dev/null"], check=True)
            
            # Renomear todos os arquivos .dot gerados para o diretório de saída
            for dot_file in glob.glob(".*.dot"):
                function_name = os.path.basename(dot_file)
                new_dot_file = f"{output_dir}/{os.path.basename(source_file)}_{opt_level}_{function_name}"
                os.rename(dot_file, new_dot_file)
                print(f"Arquivo DOT gerado: {new_dot_file}")

                # Converter o arquivo .dot em um arquivo .digraph
                digraph_file = new_dot_file.replace(".dot", ".digraph")
                os.rename(new_dot_file, digraph_file)
                print(f"Arquivo DIGRAPH gerado: {digraph_file}")

                # Converter o arquivo .digraph em PNG usando Graphviz
                png_file = digraph_file.replace(".digraph", ".png")
                try:
                    subprocess.run(["dot", "-Tpng", digraph_file, "-o", png_file], check=True)
                    print(f"Imagem PNG gerada: {png_file}")
                except subprocess.CalledProcessError:
                    print(f"Erro ao converter {digraph_file} em PNG")
                    continue
        except subprocess.CalledProcessError:
            print(f"Erro ao gerar CFG no nível {opt_level}")
            continue

def create_cfgs_from_directory(directory):
    try:
        path = os.listdir(directory)
        for root, dirs, files in os.walk(directory):
            print(files)
            for f in files:
                print(f)
                if f.endswith('.c'):
                    file_path = os.path.join(root, f)
                    generate_cfgs_for_optimization_levels(file_path, 'output_from_' + os.path.basename(directory))
                    print(file_path)
    except FileNotFoundError:
        print(f'O diretório {directory} não foi encontrado')
        return []


def main():
    if len(sys.argv) < 2:
        print("Uso: python gen_cfg.py <arquivo_c>")
        sys.exit(1)

    source_file = sys.argv[1]
    print(f"Gerando CFGs para {source_file}")
    if not os.path.isfile(source_file) or not source_file.endswith(".c"):
        print("Arquivo de entrada inválido. Forneça um arquivo .c.")
        sys.exit(1)

    generate_cfgs_for_optimization_levels(source_file, 'output_from_args')
    # create_cfgs_from_directory('src/singlesource')
    # create_cfgs_from_directory('src')


if __name__ == "__main__":
    main()