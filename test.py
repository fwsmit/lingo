from Lingo import Lingo

def test_kleuren():
    L = Lingo()
    L.antwoord = "kamer"
    L.len = 5
    assert(L.kleur_code("kamer") == "GGGGG")
    assert(L.kleur_code("kamaa") == "GGGBB")
    assert(L.kleur_code("kalen") == "GGBGB")
    assert(L.kleur_code("kzzza") == "GBBBY")
    assert(L.kleur_code("kazaa") == "GGBBB")

    L.antwoord = "lepel"
    assert(L.kleur_code("leent") == "GGYBB")
    assert(L.kleur_code("lzeze") == "GBYBY")

test_kleuren()
