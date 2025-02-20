# Instagram Reels Downloader

Este script permite baixar todos os vídeos (Reels) de uma conta pública do Instagram e salvar as descrições e hashtags associadas.

## 🚀 Funcionalidades
- Baixa todos os Reels de uma conta pública do Instagram.
- Salva os vídeos em um diretório específico.
- Garante que vídeos já baixados não sejam duplicados.
- Salva a descrição e hashtags de cada vídeo em um arquivo `.txt` correspondente.
- Implementa tratamento de exceções para evitar falhas de conexão.

## 📌 Pré-requisitos
Antes de executar o script, certifique-se de ter os seguintes itens instalados:

- Python 3.x
- `instaloader`

Para instalar a biblioteca necessária, execute:
```sh
pip install instaloader
```

## 💻 Como Usar
1. Clone este repositório ou baixe o script.
2. Execute o script e insira o nome de usuário da conta pública do Instagram quando solicitado.
```sh
python script.py
```
3. Os vídeos serão salvos no diretório:
   ```sh
   F:\programacao\python\pugno\instagram-downloader\<username>_reels
   ```

## ⚠️ Observações
- O script funciona apenas para contas públicas.
- Se o Instagram bloquear temporariamente a conexão, o script esperará 5 minutos antes de tentar novamente.
- O Instagram pode alterar sua API, o que pode afetar o funcionamento do `instaloader`.

## 📜 Licença
Este projeto é de código aberto e está sob a licença MIT. Sinta-se à vontade para modificar e melhorar o código!

---

✉️ Se tiver dúvidas ou sugestões, entre em contato!

