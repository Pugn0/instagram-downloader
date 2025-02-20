import instaloader
import os
import time
from instaloader.exceptions import ConnectionException, TwoFactorAuthRequiredException

# Inicializa o instaloader
L = instaloader.Instaloader()

# Pergunta o nome de usuário da conta pública
username = input("Digite o nome de usuário da conta pública: ")

# Solicita que o usuário cole o caminho onde deseja salvar
save_location = input("Cole o caminho onde deseja salvar os vídeos: ").strip()

# Remove aspas se o usuário colar o caminho com elas
save_location = save_location.strip('"\'')
    
# Verifica se o caminho existe
if not os.path.exists(save_location):
    print(f"O caminho {save_location} não existe.")
    exit()

# Cria a pasta para salvar os vídeos
save_path = os.path.join(save_location, f"{username}_reels")
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Define a pasta de destino como o caminho de trabalho
L.dirname_pattern = save_path

# Autenticação
insta_username = input("Digite seu nome de usuário do Instagram: ")
insta_password = input("Digite sua senha do Instagram: ")

try:
    L.login(insta_username, insta_password)
except TwoFactorAuthRequiredException:
    # Se a autenticação de dois fatores for necessária, solicite o código 2FA
    two_factor_code = input("Digite o código de autenticação de dois fatores: ")
    L.two_factor_login(two_factor_code)

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

# Carrega os códigos dos vídeos já baixados
downloaded_videos_log = os.path.join(save_path, "downloaded_videos.txt")
if os.path.exists(downloaded_videos_log):
    with open(downloaded_videos_log, "r") as f:
        downloaded_videos = set(f.read().splitlines())
else:
    downloaded_videos = set()

for post in profile.get_posts():
    if post.typename == 'GraphVideo':
        shortcode = post.shortcode
        if shortcode in downloaded_videos:
            print(f"Vídeo já baixado: {shortcode}")
            continue
        
        video_filename = f"{shortcode}.mp4"
        txt_filename = f"{shortcode}.txt"
        
        video_final_path = os.path.join(save_path, video_filename)
        txt_path = os.path.join(save_path, txt_filename)
        
        # Verifica se o vídeo já existe
        if os.path.exists(video_final_path):
            print(f"Vídeo já existe: {video_final_path}")
        else:
            # Baixa apenas o vídeo com tentativas e tratamento de exceção
            try:
                download_post_with_retries(post, save_path)
            except ConnectionException as e:
                print(f"Erro ao baixar o vídeo {shortcode}: {e}")
                continue
            
            # Verifica se o vídeo foi baixado e o renomeia para o nome final
            for filename in os.listdir(save_path):
                file_path = os.path.join(save_path, filename)
                if filename.endswith(".mp4") and filename.startswith(post.shortcode):
                    os.rename(file_path, video_final_path)
                    print(f"Vídeo baixado: {video_final_path}")
                elif not filename.endswith(".mp4") and not filename.endswith(".txt"):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            
            # Salva a descrição e as tags em um arquivo txt com o mesmo nome do vídeo
            description = post.caption or "Sem descrição"
            tags = ' '.join(post.caption_hashtags) or "Sem tags"
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"Descrição:\n{description}\n\nTags:\n{tags}")
            
            # Adiciona o código do vídeo ao log
            with open(downloaded_videos_log, "a") as f:
                f.write(shortcode + "\n")
            downloaded_videos.add(shortcode)

print(f"\nTodos os reels da conta @{username} foram salvos em {save_path}.")
