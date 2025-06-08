from PIL import Image
import os

# Diretório onde está o ícone original e onde serão salvos os novos ícones
icon_dir = '/home/ubuntu/price_tool_app/src/static/icons'

# Caminho para o ícone original
original_icon_path = os.path.join(icon_dir, 'icon-512x512.png')

# Tamanhos de ícones necessários
icon_sizes = [384, 192, 152, 144, 128, 96, 72]

# Abrir a imagem original
try:
    original_icon = Image.open(original_icon_path)
    
    # Gerar cada tamanho de ícone
    for size in icon_sizes:
        # Redimensionar a imagem mantendo a proporção
        resized_icon = original_icon.resize((size, size), Image.LANCZOS)
        
        # Salvar a imagem redimensionada
        output_path = os.path.join(icon_dir, f'icon-{size}x{size}.png')
        resized_icon.save(output_path)
        print(f"Ícone {size}x{size} gerado com sucesso: {output_path}")
    
    print("Todos os ícones foram gerados com sucesso!")
    
except Exception as e:
    print(f"Erro ao processar os ícones: {e}")
