def check_order_xml(
    narocilo_id,
    maticna,
    racun,
    sifra_artikla,
    opis_placila='Članarina',
    kolicina=1,
    cena=0.00,
    user_tax_id='',
    user_name='',
    user_address='',
    user_city='',
    user_post='',
    user_email=''
):

    order_body = f'''
        <?xml version="1.0" encoding="UTF-8"?>
        <narocilo id="{narocilo_id}" maticna="{maticna}" isoValuta="EUR" racun="{racun}" tipRacuna="1" xmlns="http://www.src.si/e-placila/narocilo/1.0">
            <opisPlacila>{opis_placila}</opisPlacila>
        <postavka sifraArtikla="{sifra_artikla}" imaProvizijo="false" konto="" podracun="" sklicPostavke="11">
            <opis>{opis_placila}</opis>
            <kolicina>{kolicina}</kolicina>
            <cena>{cena}</cena>
        </postavka>
            <kupec sifraKupca="0">
                <idZaDdv>{user_tax_id}</idZaDdv>
                <naziv>{user_name}</naziv>
                <naslov>{user_address}</naslov>
                <kraj>{user_city}</kraj>
                <posta>{user_post}</posta>
                <eposta>{user_email}</eposta>
                <poslano>false</poslano>
            </kupec>
            <referenca/>
        </narocilo>
    '''
    return order_body
