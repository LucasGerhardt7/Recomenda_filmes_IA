from django.shortcuts import render
from filme import models

# Create your views here.
def index(request):
    if request.method=='POST':
        nome = request.POST['user_nome']
        data_nascimento = request.POST['user_data']
        genero = request.POST['user_genero']

        usuario = models.Usuario(
            nome = nome,
            data_nascimento = data_nascimento,
            genero = genero
        ).save()

    return render(request, 'filme/index.html')

def home(request):
    filmesRecomendados = set()
    filmesUsuario_ids = models.FilmeRecomedado.objects.filter(idUsuario=1).values_list('idFilme', flat=True)
    filmesUsuario = models.Filme.objects.filter(pk__in=filmesUsuario_ids)
    usuario = models.Usuario.objects.get(pk=1)
    
    for filme in filmesUsuario:
        lista_filmes = recomendar_filmes(filme, usuario.anoMin, usuario.anoMax)
        for fi in lista_filmes:
            filmesRecomendados.add(fi)

    filmesRecomendados = models.Filme.objects.filter(pk__in=filmesRecomendados)
    
    return render(request, 'filme/home.html',{ 'filmesRecomendados':filmesRecomendados})

def recomendacao(request):
    if request.method=='POST':
        filmes = request.POST.getlist('idFilme')
        ano_min = request.POST['ano_min']
        ano_max = request.POST['ano_max']
        models.Usuario.objects.filter(pk=1).update(anoMin=ano_min, anoMax=ano_max)
        
        models.FilmeRecomedado.objects.filter(idUsuario=1).exclude(idFilme__in=filmes).delete()
        
        for filme in filmes:
            models.FilmeRecomedado.objects.update_or_create(
                idUsuario__pk=1, idFilme__pk=filme,
                defaults={'idUsuario':models.Usuario.objects.get(pk=1),'idFilme':models.Filme.objects.get(pk=filme)})
            
            
            
    usuarios = models.Usuario.objects.get(pk=1)
    filmesRecomendados = models.FilmeRecomedado.objects.filter(idUsuario=usuarios)
    
    filmes = models.Filme.objects.all().exclude(idFilme__in=filmesRecomendados.values('idFilme'))
    
    return render(request, 'filme/selecionarRecomendacao.html', {
                'filmes':filmes,
                'filmesRecomendados':filmesRecomendados})
    
    
def filme(request):
    if request.method=='POST':
        titulo = request.POST['filme_titulo']
        classificacao = request.POST['filme_classificacao']
        lancamento = request.POST['filme_lancamento']
        categoria = request.POST['filme_categoria']
        avaliacao = request.POST['avaliacao']
        descricao = request.POST['descricao']
        foto = request.FILES['foto']  
        
        id_categoria=models.Categoria.objects.get(pk=categoria)
        filme = models.Filme(
            titulo=titulo,
            classificacao=classificacao,
            lancamento=lancamento,
            categoria=id_categoria,
            avaliacao=avaliacao,
            descricao=descricao,
            foto=foto,
            ).save()

    categorias=models.Categoria.objects.all()

    return render(request, 'filme/filme.html', {'categorias':categorias})
    
def categoria(request):
    if request.method == 'POST':
        categoria = request.POST['categoria']
        categoria = models.Categoria(nomeCategoria=categoria).save()

    return render(request, 'filme/categoria.html')



# Função para calcular a similaridade entre dois filmes
def calcular_similaridade(filme1, filme2):
    # Conta quantos gêneros e tags são comuns entre os dois filmes
    similaridade = 0
    similaridade += (filme1.categoria.nomeCategoria == filme2.categoria.nomeCategoria)
    #similaridade += len(set(filme1['Tags']).intersection(set(filme2['Tags'])))
    # Adiciona a avaliação do filme à similaridade
    similaridade += filme2.avaliacao
    return similaridade

def recomendar_filmes(base_filme_nome, ano_min, ano_max):
    base_filme = base_filme_nome
    recomendacoes = []

    # Calculando a similaridade com cada filme no dataset dentro do intervalo de anos especificado
    df_filmes = models.Filme.objects.all()
    for filme in df_filmes:
        if filme.titulo != base_filme_nome and ano_min <= filme.lancamento.year <= ano_max:
            similaridade = calcular_similaridade(base_filme, filme)
            recomendacoes.append((filme.pk, similaridade))

    # Ordenando filmes por maior similaridade
    recomendacoes.sort(key=lambda x: x[1], reverse=True)
    # Retornando os nomes dos filmes mais similares
    return [rec[0] for rec in recomendacoes[:3]]