from Osztaly import Osztaly
d=Osztaly()

d.uj_helyszin("Egyetem ter 1")
d.uj_helyszin("Stadion Kulso")

d.helyszin_lista()

d.uj_esemeny("Egyetem ter 1",
            "20240424100000", "202404240900000", 
            "Bagossry bro", "Anna", "123")

d.uj_esemeny("Egyetem ter 2",
            "20240424100000", "202404240900000", 
            "Bagossry bro", "Anna", "123")

d.uj_esemeny("Egyetem ter 1",
             "20240424100000", "20240424090000", 
            "Bagossry bro", "Anna", "123")
d.esemeny_lista_idopont("20240424103000")
print("szia")
d.esemeny_lista()

d.uj_jegytipus("heti_felnott", 50000, "20240422000000", "20240429000000")

d.uj_jegytipus("heti_diak", 25000, "20240422000000", "20240429000000")

d.jegytipus_lista()

d.uj_vendeg("a@g.c", "anna", "20010101")
d.uj_vendeg("b@g.c", "bela", "20010101")

d.vendeg_lista()

d.like("a@g.c", "123")
d.vendeg_like_lista("a@g.c")