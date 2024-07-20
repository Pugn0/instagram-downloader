import instaloader

# Inicializa o instaloader
L = instaloader.Instaloader()

# Nome de usuário da conta pública de onde os reels serão baixados
username = "nome_de_usuario"

# Faz o login no Instagram (opcional, mas recomendado para evitar limitações)
L.login('seu_usuario', 'sua_senha')

# Baixa todos os reels
profile = instaloader.Profile.from_username(L.context, username)
for post in profile.get_posts():
    if post.typename == 'GraphVideo' and post.is_reel:
        L.download_post(post, target=f"{username}_reels")
