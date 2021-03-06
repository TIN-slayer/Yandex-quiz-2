town = {'Москва Хьюстон Дубаи': '1656841/766a66e42965517d47e8', 'Париж Токио Лас-вегас': '1533899/d88f03a71317d38313f7',
        'Сидней Мельбурн Канберра': '1652229/4b764915f09574e4c1e8',
        'Сан-Франциско Чикаго Нью-Йорк': '965417/5c68c9d56065e29d4a21',
        'Амстердам Осло Прага': '965417/70cd17190ff72bec6f20',
        'Афины Тира Крит': '1030494/6d8fe24d8775569d24f1',
        'Венеция Флоренция Рим': '1540737/5b4002334460b6316f32',
        'Волгоград Саратов Владимир': '965417/3921f88a8f202517f990',
        'Лондон Париж Москва': '1540737/50a06e2150df9e9ec2c3',
        'Мадрид Барселона Валенсия': '965417/2faf1b57a5852e1cc44c',
        'Нью-Йорк Чикаго Сан-Франциско': '965417/b481db8d9100b399357e',
        'Пекин Шанхай Сеул': '1652229/7a351740a1919f37b09f', 'Прага Берлин Варшава': '1030494/b938c0e18743b107be93',
        'Рим Милан Флоренция': '213044/1bf5a9b70ed555f5785a',
        'Рио-де-Жанейро Бразилиа Барселона': '965417/0cc19f41e8137e0f91a3',
        'Санкт-Петербург Венеция Москва': '1540737/0286fc0dac30e7c5cfd2',
        'Сингапур Сеул Куала-Лумпур': '1030494/cdfbff2f9c05ad1a0d1f',
        'Стамбул Анталья Анкара': '1652229/e3ccbc55db3bf11e30b6', 'Токио Пекин Сеул': '997614/a76304568f2dbc241444'}

quest = {
    'Выберите вариант, в котором город-столица и страна имеют одинаковые названия': 'Сингапур, Мальта, Бразилия',
    'В каком городе впервые было построено «Чертово колесо»?': 'Чикаго, Вашингтон, Нью-Йорк',
    'Название норвежского города, которое переводится как «божественная роща».': 'Осло, Лиллестрём, Ессхейм',
    'Отметьте азиатскую столицу, название которой переводится как «Красный богатырь»':
        'Улан-Батор (столица Монголии), Баку (столица Азербайджана), Ереван (столица Армении)',
    'Определите, как китайцы называют Пекин': 'Бейдзин, Пекин, Тиджир',
    'Синдбад-мореход родился в этом городе:': 'Багдаде, Стамбуле, Копенгагене',
    'Какая европейская столица имеет название, как у богини?': 'Афины, Олимпиада, Эриу',
    'Мавзолей-мечеть Тадж-Махал находится в этом городе:': 'Агре, Мубаи, Дели',
    'В каком бельгийском городе хранится ампула с кровью Иисуса Христа': 'в Брюгге, в Генке, в Алсте',
    'Этот город называют городом «желтого дьявола»:': 'Нью-Йорк, Дракар, Пекин',
    'Гайд-парк находится в этом городе:': 'В Лондоне, В Мюнхене, В Париже',
    'Столица США это:': 'Вашингтон, Бостон, Нью-Йорк', 'Где располагается Бремен?': 'Германии, Италии, Франции',
    'Этот китайский город называется «город вечного спокойствия»:': 'Сиань, Шанхай, Чунцин',
    'В этом бразильском городе находится 30-метровая фигура Христа:': 'Рио-де-Жанейро, Салвадор, Натал',
    'Отметьте город, который находится не в России:': 'Уральск, Йошкар-Ола, Вязьма',
    'Падающая башня располагается в:': 'Пизе, Милане, Падуе',
    '«Ледяная столица» мира это:': 'Харбин, Норильск, Мурманск',
    'Вспомните европейскую столицу, в которое находится огромное количество мостов:':
        'в Люксембурге, в Амстердаме, в Венеции',
    '«Столица летучих мышей» – так говорят про:': 'Остин, Анкару, Астану'}


def view_start(session, View, Inf):
    check = session.query(View).first()
    if check is None:
        for tab in range(3):
            view = View()
            if tab == 0:
                view.name = 'Угадай город по картинке'
                view.price = 1
                session.add(view)
                session.commit()
                for i in town:
                    inf = Inf()
                    inf.town = i
                    inf.town_inf = town[i]
                    inf.inst = view.id
                    inf.valid = True
                    inf.now = False
                    session.add(inf)
            if tab == 1:
                view.name = 'Вопросы по городам'
                view.price = 2
                session.add(view)
                session.commit()
                for i in quest:
                    inf = Inf()
                    inf.quest = i
                    inf.quest_ans = quest[i]
                    inf.inst = view.id
                    inf.valid = True
                    inf.now = False
                    session.add(inf)
        session.commit()
