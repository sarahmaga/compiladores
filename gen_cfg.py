import os
import subprocess
import sys

def generate_cfgs_for_optimization_levels(source_file, output_dir="output"):
    """Gera CFGs para os níveis de otimização O1, O2 e O3."""
    os.makedirs(output_dir, exist_ok=True)
    optimization_levels = ["O1", "O2", "O3"]

    for opt_level in optimization_levels:
        # Gerar bytecode LLVM com o nível de otimização especificado
        llvm_file = f"{output_dir}/{os.path.basename(source_file)}_{opt_level}.bc"
        try:
            subprocess.run(["clang", f"-{opt_level}", "-emit-llvm", "-c", source_file, "-o", llvm_file], check=True)
            print(f"Bytecode LLVM gerado: {llvm_file}")
        except subprocess.CalledProcessError:
            print(f"Erro ao gerar bytecode para o nível {opt_level}")
            continue

        # Gerar o arquivo .dot representando o CFG
        dot_file = f"{output_dir}/{os.path.basename(source_file)}_{opt_level}.dot"
        try:
            subprocess.run(["opt", "-dot-cfg", llvm_file, "-o", "/dev/null"], check=True)
            os.rename("cfg.main.dot", dot_file)
            print(f"Arquivo DOT gerado: {dot_file}")
        except subprocess.CalledProcessError:
            print(f"Erro ao gerar CFG no nível {opt_level}")
            continue

        # Converter o arquivo .dot em PNG usando Graphviz
        png_file = dot_file.replace(".dot", ".png")
        try:
            subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)
            print(f"Imagem PNG gerada: {png_file}")
        except subprocess.CalledProcessError:
            print(f"Erro ao converter {dot_file} em PNG")
            continue

def main():
    if len(sys.argv) < 2:
        print("Uso: python gen_cfg.py <arquivo_c>")
        sys.exit(1)

    source_file = sys.argv[1]
    print(f"Gerando CFGs para {source_file}")
    if not os.path.isfile(source_file) or not source_file.endswith(".c"):
        print("Arquivo de entrada inválido. Forneça um arquivo .c.")
        sys.exit(1)

    generate_cfgs_for_optimization_levels(source_file)

if __name__ == "__main__":
    main()
