# usuarios/views.py
# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Usuario


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Buscar o usuário no banco de dados
        try:
            user = Usuario.objects.get(Username=username)
            # Verificar a senha
            if user.check_password(password):
                # Armazenar informações do usuário na sessão
                request.session['user_id'] = user.CodUsuario
                request.session['user_name'] = user.Nome
                request.session['user_group'] = user.Grupo
                
                # Redirecionar com base no grupo
                if user.Grupo == 'Administradores':
                    return redirect('dashboard')
                elif user.Grupo == 'Estudantes':
                    return redirect('dashboard_estudantes')
                else:
                    return redirect('dashboard_default')
            else:
                messages.error(request, 'Senha incorreta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'usuarios/login.html')



# usuarios/views.py
from django.shortcuts import render
from .models import Usuario

def criar_usuario(nome, username, senha, grupo):
    usuario = Usuario(
        Nome=nome,
        Username=username,
        Grupo=grupo
    )
    usuario.set_password(senha)
    usuario.save()




# usuarios/views.py
from django.shortcuts import render
from .utils import login_required

@login_required
def dashboard_view(request):
    return render(request, 'usuarios/dashboard.html', {
        'user_name': request.session.get('user_name'),
    })



# usuarios/views.py
def logout_view(request):
    request.session.flush()  # Remove todos os dados da sessão
    return redirect('login')



# usuarios/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages

def gerenciar_usuarios(request):
    if request.session.get('user_group') != 'Administradores':
        return redirect('dashboard')

    usuarios = Usuario.objects.all()
    paginator = Paginator(usuarios, 10)  # 10 usuários por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'usuarios/gerenciar_usuarios.html', {'page_obj': page_obj})




import csv
from django.http import HttpResponse

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'O arquivo enviado não é um CSV.')
            return redirect('gerenciar_usuarios')

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            if 'Nome' in row and 'Username' in row and 'Grupo' in row:
                Usuario.objects.create(
                    Nome=row['Nome'],
                    Username=row['Username'],
                    Grupo=row['Grupo'],
                )

        messages.success(request, 'Usuários cadastrados com sucesso.')
        return redirect('gerenciar_usuarios')




# usuarios/views.py
from django import forms

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['Nome', 'Username', 'Senha', 'Grupo']
        widgets = {
            'Senha': forms.PasswordInput(),
        }

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['Senha'])
            usuario.save()
            return redirect('gerenciar_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})


# usuarios/views.py
from django.shortcuts import get_object_or_404

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['Senha'])
            usuario.save()
            return redirect('gerenciar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('gerenciar_usuarios')
    return render(request, 'usuarios/excluir_usuario.html', {'usuario': usuario})




def instrucoes_avaliacao(request, disciplina):
    return render(request, 'usuarios/instrucoes_avaliacao.html', {'disciplina': disciplina.capitalize()})



import os
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from usuarios.models import Usuario
from .models import Resultado


# Diretório onde os arquivos XML das questões estão armazenados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTOES_DIR = os.path.join(BASE_DIR, 'xml_storage')


def avaliacao(request, disciplina):
    # Inicialização da sessão
    if 'questao_atual' not in request.session:
        request.session['questao_atual'] = 1
        request.session['respostas'] = {}
        request.session['data_inicio'] = str(now())  # Salvar a data/hora de início

    questao_atual = request.session['questao_atual']
    respostas = request.session['respostas']

    # Caminho do arquivo XML da questão atual
    questao_file = os.path.join(QUESTOES_DIR, disciplina.lower(), f'questao_{questao_atual}.xml')

    # Verificar se o arquivo XML existe
    if not os.path.exists(questao_file):
        if questao_atual == 1:
            raise FileNotFoundError(f"Nenhum arquivo encontrado no diretório {QUESTOES_DIR}/{disciplina.lower()}/")
        return redirect('finalizar_avaliacao', disciplina=disciplina)

    # Processar o arquivo XML da questão
    try:
        tree = ET.parse(questao_file)
        root = tree.getroot()
        enunciado = root.find('enunciado').text.strip() if root.find('enunciado') is not None else ""
        imagem = root.find('imagem').text.strip() if root.find('imagem') is not None else None
        comando = root.find('comando').text.strip() if root.find('comando') is not None else ""
        alternativas = root.findall('alternativa')
    except ET.ParseError as e:
        raise ValueError(f"Erro ao processar o arquivo {questao_file}: {e}")

    # Capturar a resposta do usuário
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        if resposta:
            respostas[str(questao_atual)] = resposta
            request.session['respostas'] = respostas

        # Avançar ou retornar questão
        if 'proximo' in request.POST:
            request.session['questao_atual'] += 1
            return redirect('avaliacao', disciplina=disciplina)
        elif 'anterior' in request.POST and questao_atual > 1:
            request.session['questao_atual'] -= 1
            return redirect('avaliacao', disciplina=disciplina)
        elif 'finalizar' in request.POST:
            total_questoes = 10  # Número total de questões
            if len(respostas) < total_questoes:
                messages.error(request, 'Você deve responder todas as questões antes de finalizar a avaliação.')
                return redirect('avaliacao', disciplina=disciplina)

            # Calcular acertos
            acertos = 0
            resultado_respostas = {}
            letras = ['A', 'B', 'C', 'D', 'E']  # Mapeamento de números para letras

            for i in range(1, total_questoes + 1):
                questao_file = os.path.join(QUESTOES_DIR, disciplina.lower(), f'questao_{i}.xml')
                if os.path.exists(questao_file):
                    tree = ET.parse(questao_file)
                    root = tree.getroot()
                    alternativas = root.findall('alternativa')
                    resposta_usuario = respostas.get(str(i), None)
                    correta = [alt for alt in alternativas if alt.attrib.get('correta') == 'true']
                    if resposta_usuario:
                        # Converter resposta para letra
                        resposta_letra = letras[int(resposta_usuario) - 1]
                        respostas[str(i)] = resposta_letra

                        # Verificar se está correta
                        if correta and alternativas[int(resposta_usuario) - 1] in correta:
                            acertos += 1
                            resultado_respostas[f"Status_Q{i}"] = 1
                        else:
                            resultado_respostas[f"Status_Q{i}"] = 0
                    else:
                        resultado_respostas[f"Status_Q{i}"] = 0

            # Salvar resultado no banco de dados
            respostas_combinadas = respostas | resultado_respostas
            percentual_acertos = (acertos / total_questoes) * 100
            usuario = Usuario.objects.get(CodUsuario=request.session['user_id'])

            resultado = Resultado.objects.create(
                usuario=usuario,
                respostas=respostas_combinadas,
                acertos=acertos,
                percentual_acertos=percentual_acertos,
                data_inicio=request.session['data_inicio'],
                data_fim=now()
            )
            resultado.save()

            return redirect('finalizar_avaliacao', disciplina=disciplina)

    # Renderizar o template com as variáveis necessárias
    return render(request, 'usuarios/avaliacao.html', {
        'disciplina': disciplina.capitalize(),
        'enunciado': enunciado,
        'imagem': imagem,
        'comando': comando,
        'alternativas': alternativas,
        'questao_atual': questao_atual,
        'total_questoes': 10,
        'resposta_selecionada': respostas.get(str(questao_atual)),
    })









from django.shortcuts import render, redirect

def finalizar_avaliacao(request, disciplina):
    # Registre as respostas no banco de dados ou arquivo, se necessário
    respostas = request.session.get('respostas', {})
    usuario = request.session.get('user_name')

    # Exemplo de registro no console (substituir por salvamento real)
    print(f"Usuário: {usuario}, Disciplina: {disciplina}, Respostas: {respostas}")

    # Limpar sessão relacionada à avaliação
    if 'questao_atual' in request.session:
        del request.session['questao_atual']
    if 'respostas' in request.session:
        del request.session['respostas']

    return render(request, 'usuarios/finalizar_avaliacao.html', {'disciplina': disciplina.capitalize()})




from django.shortcuts import render

def dashboard_estudantes(request):
    if request.session.get('user_group') != 'Estudantes':
        return redirect('login')

    return render(request, 'usuarios/dashboard_estudantes.html')




from django.shortcuts import render, redirect
from .models import Resultado

def resultados_view(request):
    if request.session.get('user_group') != 'Administradores':
        return redirect('dashboard_estudantes')

    resultados = Resultado.objects.all()
    numeros_questoes = list(range(1, 11))  # Lista [1, 2, ..., 10]

    # Preprocessar dados
    resultados_processados = []
    for resultado in resultados:
        q_respostas = [resultado.respostas.get(str(i), '') for i in numeros_questoes]
        q_status = [resultado.respostas.get(f"Status_Q{i}", '') for i in numeros_questoes]
        resultados_processados.append({
            'usuario': resultado.usuario,
            'q_respostas': q_respostas,
            'q_status': q_status,
            'acertos': resultado.acertos,
            'percentual_acertos': resultado.percentual_acertos,
            'data_inicio': resultado.data_inicio,
            'data_fim': resultado.data_fim,
        })

    return render(request, 'usuarios/resultados.html', {
        'resultados': resultados_processados,
        'numeros_questoes': numeros_questoes,
    })




from .models import Usuario

def cadastrar_usuario_view(request):
    form = UsuarioForm(request.POST or None)
    usuarios = Usuario.objects.all()

    if form.is_valid():
        form.save()
        return redirect('gerenciar_usuarios')

    return render(request, 'usuarios/cadastrar_usuario.html', {
        'form': form,
        'usuarios': usuarios,
    })
