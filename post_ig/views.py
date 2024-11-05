from django.shortcuts import render
from django.http import JsonResponse    
# mudar isso antes de prod, configurar os ips permitidos
from django.views.decorators.csrf import csrf_exempt
from instagrapi import Client
from instagrapi.exceptions import (
    FeedbackRequired, ChallengeRequired, LoginRequired, PleaseWaitFewMinutes
)
from post_ig.resources import instagram
import json
from django.http import JsonResponse
from PIL import Image

def validate_and_save_img(imagem):
    if not imagem:
        return JsonResponse({'erro': 'Imagem ausente'}, status=400)

    print("Imagem recebida com nome:", imagem.name, "e tipo:", imagem.content_type)

    # Verifique se a imagem foi recebida e se está no formato esperado
    if imagem.content_type != 'image/jpeg':
        return JsonResponse({'erro': 'Formato de imagem inválido, deveria ser jpeg'}, status=400)
    
    img_path = "imagens/" + imagem.name
    img = Image.open(imagem)
    img.save(img_path)
    return img_path


def post_photo_ig(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    try:
        # Confirme se o JSON foi recebido corretamente
        dados = json.loads(request.POST.get('dados', '{}'))
        print("Dados recebidos:", dados)

        username = dados.get('username')
        password = dados.get('password')

        mensagem = dados.get('mensagem')
        legenda = dados.get('legenda')
        imagem = request.FILES.get('imagem')
        imagem_qr_code = request.FILES.get('imagem_qr_code')
        mencoes = dados.get('mencoes')

        img_path = validate_and_save_img(imagem)
        img_qr_path = validate_and_save_img(imagem_qr_code)
        cl = instagram.login(username, password)

        try:
            instagram.post_image(cl, img_path, legenda, mencoes)
            return JsonResponse({'sucesso': 'Imagem salva com sucesso'}, status=200)
        except FeedbackRequired as e:
            return JsonResponse({'erro': 
                f"Ação bloqueada temporariamente. Mensagem: {str(e)}\nNormalmente, mesmo recebendo esse erro a publicacao ainda eh postada"},
                status=400
            )
        except PleaseWaitFewMinutes as e:
            return JsonResponse({'erro': 
                f"Aguarde alguns minutos antes de tentar novamente. Mensagem: {str(e)}"},
                status=400
            )
            # Aguardará um período antes de retomar as postagens
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            return JsonResponse({'erro': 
                f"Erro inesperado: {str(e)}"},
                status=400
            )
            
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400) 


def post_carousel_ig(request):
    pass