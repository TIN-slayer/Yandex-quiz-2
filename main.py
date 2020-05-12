from flask_ngrok import run_with_ngrok
from flask import Flask, request
from data import db_session, inicial
from data.game import Game
from data.players import Player
from data.view import View
from data.inf import Inf
import logging
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)
db_session.global_init("db/quiz.sqlite")
session = db_session.create_session()
inicial.view_start(session, View, Inf)


@app.route('/', methods=['POST'])
def index():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req, restart=False):
    session = db_session.create_session()
    sp = [i.name for i in session.query(View).all()]
    if req['session']['new'] or restart:
        res['response'][
            'text'] = 'Привет! Меня зовут Алиса, викторину на тему: "Города мира". С чего начнём?'
        res['response']['buttons'] = get_suggests(sp)
        game = Game()
        game.round = 1
        game.set = 0
        game.end = False
        game.contin = True
        session.add(game)
        session.commit()
        return
    game = session.query(Game).all()
    game = game[-1]
    players = session.query(Player).filter(Player.match == game.id)
    if req['request']['original_utterance'] in sp:
        view = session.query(View).filter(View.name == req['request']['original_utterance']).first()
        game = session.query(Game)[-1]
        game.type = view.id
        session.commit()
        if players.first() is None:
            res['response'][
                'text'] = 'С игрой определились, теперь, сколько раундов будем играть?'
            res['response']['buttons'] = get_suggests(['1', '2', '3', '4', '5', 'Сам напишу!'])
            return
    if req['request']['original_utterance'] == 'Выйти из матча':
        game.end = True
        session.commit()
    if req['request']['original_utterance'] == 'Начать матч' and game.end:
        game.end = False
        session.commit()
        handle_dialog(res, req, restart=True)
        return
    elif game.end:
        res['response'][
            'text'] = 'Игра завершена.'
        res['response']['buttons'] = get_suggests(['Начать матч'])
        return
    if game.type is None:
        res['response'][
            'text'] = 'Повторите, пожалуйста, во что играем?'
        if game.contin:
            res['response']['buttons'] = get_suggests(sp)
        else:
            sp.append('Выйти из матча')
            res['response']['buttons'] = get_suggests(sp)
        return
    if game.view.rounds is None:
        if get_number(req) is None:
            res['response'][
                'text'] = 'Повторите, пожалуйста, сколько будет раундов?'
            res['response']['buttons'] = get_suggests(['1', '2', '3', '4', '5', 'Сам напишу!'])
            return
        else:
            game.view.rounds = int(get_number(req))
            session.commit()
            if players.first() is None:
                res['response'][
                    'text'] = 'С этим определились, теперь, все игроки, назовите, пожалуйста, ' \
                              'своё имя без фамилии и отчества.'
                res['response']['buttons'] = get_suggests(['и Саша, и Вася, и Коля', 'Маша и Наташа', 'Сам напишу!'])
                return

    if players.first() is None:
        gamers = get_players(req)
        if not bool(gamers):
            res['response']['text'] = \
                'Повторите, пожалуйста, кто будет играть?'
            res['response']['buttons'] = get_suggests(['и Саша, и Вася, и Коля', 'Маша и Наташа', 'Сам напишу!'])
        else:
            for name in gamers:
                player = Player()
                player.name = name
                player.round = 0
                player.match = game.id
                player.points = 0
                player.kush = 0
                player.win = 0
                player.now = False
                session.add(player)
                session.commit()
    if players.first() is not None:
        game.contin = True
        session.commit()
        if req['request']['original_utterance'] == 'Закончить игру' or game.round > game.view.rounds:
            quit(res, req, players, session, game)
        else:
            if game.view.name == 'Угадай город по картинке':
                play_towns(res, req)
            elif game.view.name == 'Вопросы по городам':
                play_quests(res, req)


def play_towns(res, req, fin=False):
    session = db_session.create_session()
    itog = ''
    game = session.query(Game).all()
    game = game[-1]
    player = session.query(Player).filter(Player.match == game.id, Player.round == game.round - 1).first()
    check = session.query(Player).filter(Player.match == game.id).first()
    dano1 = session.query(Inf).filter(Inf.inst == game.view.id).all()
    dano = []
    for i in dano1:
        if i.valid is True:
            dano.append(i)
    if not bool(dano):
        dano1 = session.query(Inf).filter(Inf.inst == game.view.id).all()
        dano = []
        for i in dano1:
            i.valid = True
            if i.now is not True:
                dano.append(i)
        session.commit()
    if check.round != 0:
        city = get_city(req)
        town = session.query(Inf).filter(Inf.inst == game.view.id).all()
        for i in town:
            if i.now is True:
                town = i
                break
        town1 = town.town.split()[0].lower()
        player1 = session.query(Player).filter(Player.match == game.id).all()
        for i in player1:
            if i.now is True:
                player1 = i
                break
        print(city, town1)
        if city == town1:
            itog = f'Молодец, ответ правильный, + {game.view.price} очко! '
            num = int(player1.points)
            player1.points = num + int(game.view.price)
            session.commit()
        else:
            itog = 'Извини, но ответ неправильный. '
        town.now = False
        player1.now = False
        session.commit()
    if fin:
        return itog
    else:
        player.round += 1
        player.now = True
        town2 = session.query(Inf).filter(Inf.inst == game.view.id).all()
        for i in town2:
            if i.now is True:
                i.now = False
                break
        town = random.choice(dano)
        town.now = True
        town.valid = False
        session.commit()
        variant = town.town.split()
        random.shuffle(variant)
        variant.append('Закончить игру')
        res['response']['text'] = 'Error'
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['image_id'] = town.town_inf
        res['response']['card'][
            'title'] = f'{itog}{game.round} раунд, {player.name.title()}, угадай, что это за город на фотографии?'
        res['response']['buttons'] = get_suggests(variant)
        player = session.query(Player).filter(Player.match == game.id, Player.round == game.round - 1).first()
        if player is None:
            game.round += 1
            session.commit()
    session.commit()


def play_quests(res, req, fin=False):
    session = db_session.create_session()
    itog = ''
    game = session.query(Game).all()
    game = game[-1]
    player = session.query(Player).filter(Player.match == game.id, Player.round == game.round - 1).first()
    check = session.query(Player).filter(Player.match == game.id).first()
    dano1 = session.query(Inf).filter(Inf.inst == game.view.id).all()
    dano = []
    for i in dano1:
        if i.valid is True:
            dano.append(i)
    if not bool(dano):
        dano1 = session.query(Inf).filter(Inf.inst == game.view.id).all()
        dano = []
        for i in dano1:
            i.valid = True
            if i.now is not True:
                dano.append(i)
        session.commit()
    if check.round != 0:
        ans = req['request']['original_utterance'].lower()
        quest = session.query(Inf).filter(Inf.inst == game.view.id).all()
        for i in quest:
            if i.now is True:
                quest = i
                break
        print(quest.quest_ans)
        quest1 = quest.quest_ans.split(', ')[0].lower()
        player1 = session.query(Player).filter(Player.match == game.id).all()
        for i in player1:
            if i.now is True:
                player1 = i
                break
        if ans == quest1:
            itog = f'Молодец, ответ правильный, + {game.view.price} очка! '
            num = int(player1.points)
            player1.points = num + int(game.view.price)
            session.commit()
        else:
            itog = 'Извини, но ответ неправильный. '
        quest.now = False
        player1.now = False
        session.commit()
    if fin:
        return itog
    else:
        player.round += 1
        player.now = True
        quest2 = session.query(Inf).filter(Inf.inst == game.view.id).all()
        for i in quest2:
            if i.now is True:
                i.now = False
                break
        quest = random.choice(dano)
        quest.now = True
        quest.valid = False
        session.commit()
        res['response']['text'] = f'{itog}{game.round} раунд, {player.name.title()}, {quest.quest}'
        variant = quest.quest_ans.split(', ')
        random.shuffle(variant)
        variant.append('Закончить игру')
        res['response']['buttons'] = get_suggests(variant)
        player = session.query(Player).filter(Player.match == game.id, Player.round == game.round - 1).first()
        if player is None:
            game.round += 1
            session.commit()
    session.commit()


def get_city(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            return entity['value'].get('city', None)


def get_number(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.NUMBER':
            if int(entity['value']) > 0 and int(entity['value']) < 100:
                return entity['value']
    return None


def get_players(req):
    gamers = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            gamers.append(entity['value'].get('first_name', None))
    return gamers


def get_suggests(sp):
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in sp
    ]
    return suggests


def quit(res, req, players, session, game):
    if game.view.name == 'Угадай город по картинке':
        itog = play_towns(res, req, fin=True)
    elif game.view.name == 'Вопросы по городам':
        itog = play_quests(res, req, fin=True)
    pobeda = ''
    winners = []
    maxim = max(players.all(), key=lambda x: x.points).points
    game = session.query(Game).all()[-1]
    game.set += 1
    game.round = 1
    game.view.rounds = None
    game.type = None
    game.contin = False
    for i in players:
        if i.points == maxim:
            i.win += 1
            winners.append(i.name.title())
        i.kush += i.points
        i.points = 0
        i.round = 0
    if len(winners) == 1:
        pobeda = 'Победил(а)'
    elif len(winners) > 1:
        pobeda = 'Победили'
    inf = session.query(Inf).all()
    for i in inf:
        i.valid = True
        i.now = False
    session.commit()
    winners2 = []
    winners3 = []
    game = session.query(Game).all()[-1]
    sets = game.set
    players0 = session.query(Player).filter(Player.match == game.id).all()
    maxim2 = max(players0, key=lambda x: x.kush).kush
    maxim3 = max(players0, key=lambda x: x.win).win
    for i in players0:
        if i.kush == maxim2:
            winners2.append(i.name.title())
        if i.win == maxim3:
            winners3.append(i.name.title())
    session.commit()
    sp = [i.name for i in session.query(View).all()]
    sp.append('Выйти из матча')
    res['response']['text'] = f'{itog} {pobeda} в раунде {", ".join(winners)}. ' \
        f'Из {sets} игр(ы) по общему кол-ву очков впереди {", ".join(winners2)}, ' \
        f'а по победам в игре - {", ".join(winners3)}. В какую следующую игру сыграем?'
    res['response']['buttons'] = get_suggests(sp)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
