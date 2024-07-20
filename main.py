import instaloader
import os

# Inicializa o instaloader
L = instaloader.Instaloader()

# Pergunta o nome de usuário da conta pública
username = input("Digite o nome de usuário da conta pública: ")

# Pergunta o local onde deseja salvar os vídeos
save_location = input("Digite o caminho onde deseja salvar os vídeos: ")

# Cria a pasta para salvar os vídeos, se não existir
save_path = os.path.join(save_location, f"{username}_reels")
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Faz o login no Instagram (opcional, mas recomendado para evitar limitações)
# Descomente e preencha com suas credenciais se desejar fazer login
# L.login('seu_usuario', 'sua_senha')

# Baixa todos os reels
profile = instaloader.Profile.from_username(L.context, username)
for post in profile.get_posts():
    # Verifica se o post é um vídeo e se a URL contém 'reel'
    if post.typename == 'GraphVideo' and 'reel' in post.url:
        L.download_post(post, target=save_path)

print(f"Todos os reels da conta @{username} foram salvos em {save_path}.")
