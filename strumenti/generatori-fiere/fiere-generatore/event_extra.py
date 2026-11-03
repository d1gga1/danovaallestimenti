# -*- coding: utf-8 -*-
# Campi consigliati da Google per gli eventi (Search Console, 10 ottobre 2026):
# organizer, performer, image (offers omesso: vedi sotto). Usato da nuove_common.event_node e da
# patch_eventi.py (che li aggiunge alle pagine gia' generate).
IMG="https://danova-tech.com/assets/img/og-cover.jpg"
def arricchisci(ev):
    n=ev.get("name",""); site=ev.get("url")
    org={"@type":"Organization","name":n}
    if site: org["url"]=site
    ev.setdefault("organizer",org)
    ev.setdefault("performer",dict(org))
    ev.setdefault("image",[IMG])
    # Niente "offers": un Offer senza price/priceCurrency/validFrom genera 3 avvisi in
    # Search Console (17 ottobre 2026) e non conosciamo i prezzi reali dei biglietti
    # delle fiere. Meglio non dichiararli che inventarli.
    return ev
