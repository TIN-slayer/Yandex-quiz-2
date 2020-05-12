town = {'москва': '1656841/766a66e42965517d47e8', 'нью-йорк': '1030494/4e72af143eb18c0ca314',
        'париж': '1533899/d88f03a71317d38313f7', 'барселона': '965417/19b638cc48b5c8ab10a2',
        'тайбей': '1030494/d859ae597a06e5f63530', 'ванкувер': '937455/7a2e7b57b7b3fc0f6b9c',
        'вена': '1652229/414debb789fc4a08af13', 'флоренция': '1540737/d8736e7da15f64b410ac',
        'амстредам': '1540737/42415a72fa053b03bb60', 'чикаго': '1652229/52757ffceaf501795f11',
        'сиэтл': '1030494/13dcd11378e9975d4a53', 'сан-паулу': '1652229/da09a684de9a3dbff12f',
        'киев': '1030494/8906b0f61027b712b9b6', 'милан': '1030494/aa5d61dc0a39a2b41db2',
        'стамбул': '1540737/b9306dd08530809ea2bb', 'токио': '965417/e674464a83da53007fc7',
        'венеция': '1030494/c45fbf916113a3ae0a23', 'рим': '937455/1300dd61b67f0c2b9d6b',
        'сан-франциско': '965417/5c68c9d56065e29d4a21', 'сингапур': '965417/07916628ddafebca62de',
        'лондон': '1030494/4b3b98c73f7af2a3952a', 'сидней': '1652229/4b764915f09574e4c1e8'}


def view_start(session, View, Inf):
    check = session.query(View).first()
    if check is None:
        for tab in range(3):
            view = View()
            if tab == 0:
                view.name = 'Towns'
                view.price = 2
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
        session.commit()
