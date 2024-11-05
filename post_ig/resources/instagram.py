from instagrapi import Client
from instagrapi.exceptions import (
    FeedbackRequired, ChallengeRequired, LoginRequired, PleaseWaitFewMinutes
)
from instagrapi.types import Usertag
import json

def login(username, password):
    cl = Client()
    cl.login(username, password)
    return cl

def post_image(cl, img_path, description, mentions):
    #mencoes = json.loads(mentions)
    usertags = []
    description += '\n'
    for i in mentions:
        usertags.append(cl.user_info_by_username(i))
        description+= '@'+i+'\n'
    try:
        # Post the image
        media = cl.photo_upload(
            img_path, 
            description,
            usertags = [Usertag(user=i, x=0.5, y=0.5) for i in usertags]
        )
        print(f"Postagem bem-sucedida: {media.dict()}")
        return 1  # Retorna a mídia se o upload for bem-sucedido
    except FeedbackRequired as e:
        print(f"Erro: Ação bloqueada temporariamente. Mensagem: {str(e)}\nNormalmente, mesmo recebendo esse erro a publicacao ainda eh postada")
        raise e
        # Aguarde ou tente outra abordagem
    except ChallengeRequired as e:
        print(f"Desafio de segurança necessário. Mensagem: {str(e)}")
        raise e
        # Pode ser necessário resolver o desafio manualmente
    except LoginRequired as e:
        print(f"Erro: É necessário relogar. Mensagem: {str(e)}")
        raise e
        # Relogue e tente novamente
    except PleaseWaitFewMinutes as e:
        print(f"Erro: Aguarde alguns minutos antes de tentar novamente. Mensagem: {str(e)}")
        raise e
        # Aguardará um período antes de retomar as postagens
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        raise e
        # Para erros não previstos
    return 0  # Indica falha no upload

def post_carousel(image_paths, description):
    print(image_paths)
    # Upload the images to a carousel (list of file paths)

    # Post the carousel
    try:
        media = cl.album_upload(image_paths, description)
        print(f"Postagem bem-sucedida: {media}")
        return 1 
    except FeedbackRequired as e:
        print(f"Erro: Ação bloqueada temporariamente. Mensagem: {str(e)}")
        return 2
    except ChallengeRequired as e:
        print(f"Desafio de segurança necessário. Mensagem: {str(e)}")
        return e
    except LoginRequired as e:
        print(f"Erro: É necessário relogar. Mensagem: {str(e)}")
        return e
    except PleaseWaitFewMinutes as e:
        print(f"Erro: Aguarde alguns minutos antes de tentar novamente. Mensagem: {str(e)}")
        return e
   


if __name__ == '__main__':
    post_image('imagens/qr_spotted18.jpg', 'descricao')