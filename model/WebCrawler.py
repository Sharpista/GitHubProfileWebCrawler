import requests
from bs4 import BeautifulSoup
import pygame.image
from pygame import font
import io


class Contexto:
    terminou = False
    tela = None
    largura_tela = 800
    altura_tela = 600


class Perfil:
    nome = ''
    apelido = ''
    biografia = ''
    foto = ''
    qtd = ''
    repo = []


def repositorios(contexto):
    dicRepo = {}
    ww = []
    tela = contexto.tela
    count = 100
    response = requests.get('https://github.com/{}?tab=repositories'.format("Sharpista"))
    if response.status_code == 404:
        return None
    else:

        soup = BeautifulSoup(response.text, 'html.parser')

        re = soup.find(id='user-repositories-list')
        repnome = re.find_all('li',
                              class_='col-12 d-flex width-full py-4 border-bottom color-border-secondary public source')

        for r in repnome:
            titulo = r.find('a').get_text().replace('\n', '')
            subtitulo = r.find(class_='col-9 d-inline-block text-gray mb-2 pr-4')
            star = r.find(class_='muted-link mr-3')
            if subtitulo is None:
                descricao = 'Não há o que mostrar'
                dicRepo = {'nome': titulo, 'subtitulo': descricao, 'star': star}
            else:
                d = subtitulo.text.replace('\n', '')
                dicRepo = {'nome': titulo, 'subtitulo': d, 'star': star}

        ww.append(dicRepo)
        for obj in ww:
            escreve_tela(str(obj), tela, count, 500)
            count += 60


def perfil(nome):
    response = requests.get('https://github.com/{}?tab=repositories'.format(nome))
    if response.status_code == 404:
        print('Nome invalido')
        return None

    else:
        ctx = Contexto()
        soup = BeautifulSoup(response.text, 'html.parser')
        nome = soup.find_all(class_="p-name")
        apelido = soup.find_all(class_="p-nickname")
        biografia = soup.find_all(class_="p-note user-profile-bio mb-3 js-user-profile-bio f4")
        foto = soup.find("img", class_="avatar avatar-user width-full border bg-white")
        qtdRepositorios = soup.find(class_="Counter")
        repo = []

        for tag in soup.find_all(class_="wb-break-all"):
            repo.append(tag.get_text().replace('\n', ''))

        perfis = {
            'nome': nome[0].get_text(),
            'apelido': apelido[0].get_text(),
            'biografia': biografia[0].get_text(),
            'foto': foto['src'],
            'qtdRepositorio': qtdRepositorios.get_text(),
            'repositorios': repo

        }

        ctx.perfis = perfis

        return ctx


def escrever_informacoes(contexto):
    box = contexto.tela
    nome = [contexto.perfis['nome']]
    lista = [contexto.perfis['apelido'], contexto.perfis['biografia'],
             contexto.perfis['qtdRepositorio']]
    res = requests.get(contexto.perfis['foto'])
    img = io.BytesIO(res.content)
    t = pygame.image.load(img)
    q = pygame.Rect((50, 50, 50, 50))
    box.blit(pygame.transform.scale(t, (200, 200)), q)
    repo = contexto.perfis['repositorios']
    start_button = pygame.draw.rect(contexto.tela, TEXTO, (675, 20, 100, 50))
    count = 100
    count2 = 300
    count3 = 0
    for n in nome:
        escreve_tela3(n, box, count3, 300)
        count3 += 60
    for f in lista:
        escreve_tela2(f, box, count, 300)
        count += 60
    for n in repo:
        escreve_tela(str(n), box, count2, 300)
        count2 += 60


FUNDO = (0, 0, 0)
TEXTO = (255, 255, 255)
x = 400
y = 300
cor = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 50.2, 0)


def montarTela(contexto):
    escrever_informacoes(contexto)
    # repositorios(contexto)


def escreve_tela(texto, tela, pos_y, pos_x):
    pygame.font.init()
    Tahoma = pygame.font.SysFont('Tahoma', 22)
    text = Tahoma.render(texto, True, TEXTO)
    tela.blit(text, (pos_x, pos_y))


def escreve_tela2(texto, tela, pos_y, pos_x):
    pygame.font.init()
    Arial = pygame.font.SysFont('Arial', 21)
    text = Arial.render(texto, True, (255, 0, 0))
    tela.blit(text, (pos_x, pos_y))


def escreve_tela3(texto, tela, pos_y, pos_x):
    pygame.font.init()
    Arial = pygame.font.SysFont('Arial', 21)
    text = Arial.render(texto, True, (0, 255, 0))
    tela.blit(text, (pos_x, pos_y))


def main():
    pygame.init()
    fonte = pygame.font.Font(pygame.font.get_default_font(), 36)
    a = pygame.image.load('GoogleChrome.png')
    pygame.display.set_icon(a)
    pygame.display.set_caption('Web Crawler')
    m = input('Digite o nome do úsuario que deseja buscar: ')
    contexto = perfil(m)
    if not contexto:
        return
    tela = pygame.display.set_mode((contexto.largura_tela, contexto.altura_tela))
    clock = pygame.time.Clock()
    contexto.tela = tela

    while not contexto.terminou:

        pygame.display.update()
        tela.fill(FUNDO)

        montarTela(contexto)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                contexto.terminou = True

        clock.tick(60)

    pygame.display.quit()

    pygame.quit()


if __name__ == '__main__':
    main()
