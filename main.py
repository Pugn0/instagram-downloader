import instaloader
import os
import time
from instaloader.exceptions import ConnectionException

# Inicializa o instaloader
L = instaloader.Instaloader()

# Pergunta o nome de usuário da conta pública
username = input("Digite o nome de usuário da conta pública: ")

# Define o caminho fixo para salvar os vídeos
save_location = r"F:\programacao\python\pugno\instagram-downloader"

# Cria a pasta para salvar os vídeos, se não existir
save_path = os.path.join(save_location, f"{username}_reels")
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Define a pasta de destino como o caminho de trabalho
L.dirname_pattern = save_path

# Baixa todos os reels
profile = instaloader.Profile.from_username(L.context, username)

# Função para baixar o post com tentativas e tratamento de exceção
def download_post_with_retries(post, target):
    while True:
        try:
            L.download_post(post, target=target)
            break
        except ConnectionException as e:
            if "401 Unauthorized" in str(e):
                print("Recebeu 401 Unauthorized. Esperando 5 minutos antes de tentar novamente...")
                time.sleep(300)  # Espera 5 minutos antes de tentar novamente
            else:
                raise e

for post in profile.get_posts():
    if post.typename == 'GraphVideo':
        shortcode = post.shortcode
        video_filename = f"{shortcode}.mp4"
        txt_filename = f"{shortcode}.txt"
        
        video_final_path = os.path.join(save_path, video_filename)
        txt_path = os.path.join(save_path, txt_filename)
        
        # Verifica se o vídeo já existe
        if os.path.exists(video_final_path):
            print(f"Vídeo já existe: {video_final_path}")
        else:
            # Baixa apenas o vídeo com tentativas e tratamento de exceção
            download_post_with_retries(post, save_path)
            
            # Verifica se o vídeo foi baixado e o renomeia para o nome final
            for filename in os.listdir(save_path):
                file_path = os.path.join(save_path, filename)
                if filename.endswith(".mp4") and filename.startswith(post.shortcode):
                    os.rename(file_path, video_final_path)
                    print(f"Vídeo baixado: {video_final_path}")
                elif not filename.endswith(".mp4") and not filename.endswith(".txt"):
                    os.remove(file_path)
            
            # Salva a descrição e as tags em um arquivo txt com o mesmo nome do vídeo
            description = post.caption or "Sem descrição"
            tags = ' '.join(post.caption_hashtags) or "Sem tags"
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"Descrição:\n{description}\n\nTags:\n{tags}")

print(f"\nTodos os reels da conta @{username} foram salvos em {save_path}.")
