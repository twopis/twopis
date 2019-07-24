# This notes the author and title of the Icelandic texts, and is used by
# parseIcelandicTexts.py.

icepahcList = [
    {"id": "1325.arni.nar-sag", "author": "Anon_Árna", "title": "Árna_Saga_Biskups"},
    {"id": "1450.bandamenn.nar-sag", "author": "Anon_Bandamanna_K", "title": "Bandamanna_Saga_K"},
    {"id": "1450.ectorssaga.nar-sag", "author": "Anon_Ectors", "title": "Ectors_Saga"},
    {"id": "1350.finnbogi.nar-sag", "author": "Anon_Finnboga", "title": "Finnboga_Saga_Ramma"},
    {"id": "1270.gragas.law-law", "author": "Anon_Grágás", "title": "Grágás"},
    {"id": "1400.gunnar2.nar-sag", "author": "Anon_Gunnars", "title": "Gunnars_Saga_Keldugnúpsfífls"},
    {"id": "1150.homiliubok.rel-ser", "author": "Anon_Hómilíubók", "title": "Íslensk_Hómilíubók"},
    {"id": "1650.illugi.nar-sag", "author": "Anon_Illuga", "title": "Illuga_Saga_Tagldarbana"},
    {"id": "1480.jarlmann.nar-sag", "author": "Anon_Jarlmanns", "title": "Jarlmanns_Saga_og_Hermanns"},
    {"id": "1210.jartein.rel-sag", "author": "Anon_Jarteinabók", "title": "Jarteinabók"},
    {"id": "1260.jomsvikingar.nar-sag", "author": "Anon_Jómsvíkinga", "title": "Jómsvíkinga_Saga"},
    # {"id": "1450.judit.rel-bib", "author": "Anon_Júditarbók", "title": "Júditarbók"}, # Bible translation
    # {"id": "1475.aevintyri.nar-rel", "author": "Anon_Miðaldaævintýri", "title": "Miðaldaævintýri"}, # Translation (English)
    {"id": "1275.morkin.nar-his", "author": "Anon_Morkinskinna", "title": "Morkinskinna"},
    {"id": "1350.marta.rel-sag", "author": "Anon_Mörtu", "title": "Mörtu_Saga_og_Maríu_Magdalenu"},
    {"id": "1680.skalholt.nar-rel", "author": "Anon_Sögu-þáttur", "title": "Sögu-þáttur"},
    {"id": "1450.vilhjalmur.nar-sag", "author": "Anon_Vilhjálms", "title": "Vilhjálms_Saga_Sjóðs"},
    {"id": "1400.viglundur.nar-sag", "author": "Anon_Víglundar", "title": "Víglundar_Saga"},
    {"id": "1210.thorlakur.rel-sag", "author": "Anon_Þorláks", "title": "Þorláks_Saga_Helga"},
    {"id": "1593.eintal.rel-oth", "author": "Arngrímur_Jónsson", "title": "Eintal_Sálarinnar_Við_Sjálfa_Sig"},
    {"id": "1861.orrusta.nar-fic", "author": "Benedikt_Gröndal", "title": "Sagan_af_Heljarslóðarorrustu"},
    # {"id": "1525.erasmus.nar-sag", "author": "Björn_Þorleifsson", "title": "Erasmus_Saga"}, # Translation (Low German)
    # {"id": "1525.georgius.nar-rel", "author": "Björn_Þorleifsson", "title": "Georgíus_Sag"}, # Translation (Low German)
    # {"id": "1300.alexander.nar-sag", "author": "Brandur_Jónsson", "title": "Alexanders_Saga"}, # Translation from Latin
    {"id": "1908.ofurefli.nar-fic", "author": "Einar_H_Kvaran", "title": "Ofurefli"},
    {"id": "2008.ofsi.nar-sag", "author": "Einar_Kárason", "title": "Ofsi"},
    {"id": "1888.grimur.nar-fic", "author": "Gestur_Pálsson", "title": "Grímur_Kaupmaður_Deyr"},
    {"id": "1883.voggur.nar-fic", "author": "Gestur_Pálsson", "title": "Hans_Vöggur"},
    {"id": "1888.vordraumur.nar-fic", "author": "Gestur_Pálsson", "title": "Vordraumur"},
    {"id": "1830.hellismenn.nar-sag", "author": "Gísli_Konráðsson", "title": "Hellismanna_Saga"},
    {"id": "2008.mamma.nar-fic", "author": "Guðmundur_Andri_Thorsson", "title": "Segðu_mömmu_að_mér_líði_vel"},
    {"id": "1611.okur.rel-oth", "author": "Guðmundur_Einarsson", "title": "Okur"},
    {"id": "1675.modars.nar-fic", "author": "Halldór_Þorbergsson", "title": "Móðars_þáttur"},
    {"id": "1920.arin.rel-ser", "author": "Haraldur_Níelsson", "title": "Árin_og_Eilífðin"},
    {"id": "1725.biskupasogur.nar-rel", "author": "Jón_Halldórsson", "title": "Biskupasögur_Jóns_prófasts_Halldórssonar_í_Hítardal"},
    {"id": "1659.pislarsaga.bio-aut", "author": "Jón_Magnússon", "title": "Píslarsaga_séra_Jóns_Magnússonar"},
    {"id": "1790.fimmbraedra.nar-sag", "author": "Jón_Oddsson_Hjaltalín", "title": "Fimmbræðra_Saga"},
    {"id": "1661.indiafari.bio-tra", "author": "Jón_Ólafsson_Indíafari", "title": "Reisubók_Jóns_Ólafssonar_Indíafara"},
    {"id": "1745.klim.nar-fic", "author": "Jón_Ólafsson_úr_Grunnavík", "title": "Nikulás_Klím"},
    {"id": "1791.jonsteingrims.bio-aut", "author": "Jón_Steingrímsson", "title": "Ævisaga"},
    {"id": "1850.piltur.nar-fic", "author": "Jón_Thoroddsen", "title": "Piltur_og_Stúlka"},
    {"id": "1907.leysing.nar-fic", "author": "Jón_Trausti", "title": "Leysing"},
    {"id": "1720.vidalin.rel-ser", "author": "Jón_Þorkelsson_Vídalín", "title": "Vídalínspostilla"},
    {"id": "1675.armann.nar-fic", "author": "Jón_Þorláksson", "title": "öguþáttur_af_Ármanni_og_Þorsteini_Gála"},
    {"id": "1835.jonasedli.sci-nat", "author": "Jónas_Hallgrímsson", "title": "Um_eðli_og_uppruna_jarðarinnar"},
    # {"id": "1540.ntacts.rel-bib", "author": "Oddur_Gottskálksson", "title": "Nýja_Testamenti_Odds_Gottskálkssonar_Acts"}, # Translation
    # {"id": "1540.ntjohn.rel-bib", "author": "Oddur_Gottskálksson", "title": "Nýja_Testamenti_Odds_Gottskálkssonar_John"}, # Translation
    {"id": "1628.olafuregils.bio-tra", "author": "Ólafur_Egilsson", "title": "Reisubók_séra_Ólafs_Egilssonar"},
    {"id": "1985.sagan.nar-fic", "author": "Pétur_Gunnarsson", "title": "Sagan_öll"},
    {"id": "1859.hugvekjur.rel-ser", "author": "Pétur_Pétursson", "title": "Fimtíu_hugvekjur_út_af_pínu_og_dauða_Drottins_vors_Jesú_Krists"},
    {"id": "1250.thetubrot.nar-sag", "author": "Snorri_Sturluson", "title": "Þetubrot_Egils_Sögu"},
    {"id": "1250.sturlunga.nar-sag", "author": "Sturla_Þórðarson", "title": "Íslendinga_Saga"},
    {"id": "1150.firstgrammar.sci-lin", "author": "The_First_Grammarian", "title": "Fyrsta_Málfræðiritgerðin"},
    {"id": "1882.torfhildur.nar-fic", "author": "Torfhildur_Hólm", "title": "Brynjólfur_Sveinsson_Biskup"},
    {"id": "1902.fossar.nar-fic", "author": "Þorgils_Gjallandi", "title": "Upp_við_fossa"},
    #{"id": "1630.gerhard.rel-oth", "author": "Þorlákur_Skúlason", "title": "Fimmtíu_heilagar_hugvekjur_Meditationes_sacrae"}, # Translation
    {"id": "1675.magnus.bio-oth", "author": "Þorsteinn_Björnsson", "title": "Um_ætt_Magnúsar_Jónssonar"},
    {"id": "1985.margsaga.nar-fic", "author": "Þórarinn_Eldjárn", "title": "Margsaga"},
    #{"id": "1350.bandamennM.nar-sag", "author": "Anon_Bandamanna_M", "title": "Bandamanna_Saga_M"}, # Duplicate
    #{"id": "1310.grettir.nar-sag", "author": "Anon_Grettis", "title": "Grettis_Saga_Ásmundarsonar"}, # Duplicate
]

sagasList = [
    {"id": "F1E", "title": "Heimskringla"},
    #{"id": "F01", "title": "Bandamanna saga - Konungsbók"}, # dup in icepahc
    {"id": "F02", "title": "Bárðar saga Snæfellsáss"},
    #{"id": "F03", "title": "Bjarnar saga Hítdælakappa"},
    {"id": "F04", "title": "Brennu-Njáls saga"},
    {"id": "F05", "title": "Droplaugarsona saga"},
    {"id": "F06", "title": "Egils saga Skalla-Grímssonar"},
    {"id": "F07", "title": "Eiríks saga rauða"},
    {"id": "F08", "title": "Eyrbyggja saga"},
    #{"id": "F09", "title": "Finnboga saga ramma"}, # dup in icepahc
    {"id": "F0A", "title": "Fljótsdæla saga"},
    {"id": "F0B", "title": "Flóamanna saga"},
    {"id": "F0C", "title": "Fóstbræðra saga"},
    {"id": "F0E", "title": "Gísla saga Súrssonar - lengri gerð"},
    #{"id": "F0D", "title": "Gísla saga Súrssonar - styttri gerð"},
    {"id": "F0F", "title": "Grettis saga Ásmundarsonar"},
    {"id": "F0K", "title": "Gunnlaugs saga ormstungu"},
    {"id": "F0G", "title": "Grænlendinga saga"},
    #{"id": "F0H", "title": "Grænlendinga þáttur"},
    {"id": "F0I", "title": "Gull-Þóris saga"},
    #{"id": "F0J", "title": "Gunnars saga Keldugnúpsfífls"}, # dup in icepahc
    {"id": "F0L", "title": "Hallfreðar saga (eftir Möðruvallabók)"},
    #{"id": "F0M", "title": "Hallfreðar saga (úr Ólafs sögu Tryggvasonar hinni mestu)"},
    {"id": "F0N", "title": "Harðar saga og Hólmverja"},
    #{"id": "F0O", "title": "Hávarðar saga Ísfirðings "},
    {"id": "F0P", "title": "Heiðarvíga saga"},
    {"id": "F0Q", "title": "Hrafnkels saga Freysgoða"},
    #{"id": "F0R", "title": "Hænsna-Þóris saga "},
    #{"id": "F1D", "title": "Íslendinga þættir"},
    #{"id": "F0T", "title": "Jökuls þáttur Búasonar"},
    {"id": "F0S", "title": "Kjalnesinga saga"},
    {"id": "F0U", "title": "Kormáks saga"},
    {"id": "F0V", "title": "Króka-Refs saga"},
    {"id": "F0X", "title": "Laxdæla saga"},
    {"id": "F11", "title": "Ljósvetninga saga - A-gerð"},
    #{"id": "F0Y", "title": "Ljósvetninga saga - C-gerð "},
    {"id": "F12", "title": "Reykdæla saga"},
    {"id": "F13", "title": "Svarfdæla saga"},
    {"id": "F14", "title": "Valla-Ljóts saga"},
    {"id": "F15", "title": "Vatnsdæla saga "},
    {"id": "F16", "title": "Víga-Glúms saga "},
    #{"id": "F17", "title": "Víglundar saga"}, # dup in icepahc
    {"id": "F18", "title": "Vopnfirðinga saga"},
    {"id": "F1A", "title": "Þorsteins saga hvíta"},
    {"id": "F1B", "title": "Þorsteins saga Síðu-Hallssonar"},
    {"id": "F19", "title": "Þórðar saga hreðu"},
    {"id": "F1C", "title": "Ölkofra saga"},
    {"id": "F1G", "title": "Landnámabók - Sturlubók"},
    {"id": "F1F", "title": "Sturlunga"},
]

modernBookList = [
    {"id": "B0A", "author": "Ari Kristján Sæmundssen", "title": "Með stein í skónum"}, # Short Novel (?)
    {"id": "B0B", "author": "Arnaldur Birgir Konráðsson", "title": "Boot camp:grunnþjálfun"}, # Exercise book
    {"id": "B0C", "author": "Arnaldur Indriðason", "title": "Mýrin"}, # Novel
    {"id": "B0D", "author": "Arnþór Gunnarsson", "title": "Guðni í Sunnu:endurminningar og uppgjör"}, # Vaguely autobiographical about author's time in business
    {"id": "B0E", "author": "Auður Jónsdóttir", "title": "Vetrarsól"}, # Novel
    {"id": "B0F", "author": "Álfheiður Steinþórsdóttir", "title": "Ást í blíðu og stríðu:sálfræðibók um sambönd"}, # Guide to a healthy marriage
    {"id": "B0G", "author": "Ármann Jakobsson", "title": "Staður í nýjum heimi:konungasagan Morkinskinna"}, # Historical study on Morkinskinna
    {"id": "B0H", "author": "Árni Bergmann", "title": "Glíman við Guð"}, # Fiction, collection of thoughts on god (some poetry?)
    {"id": "B0I", "author": "Árni Björnsson", "title": "Þorrablót"}, # Nonfiction on Thorrablot festival
    {"id": "B0J", "author": "Bergþór Pálsson", "title": "Vinamót:um veislur og borðsiði"}, # Nonfiction on how to host a good party
    {"id": "B0K", "author": "Birgitta Jónsdóttir", "title": "Dagbók kamelljónsins"}, # Novel
    {"id": "B0L", "author": "Björn Hróarsson", "title": "Hellahandbókin:leiðsögn um 77 íslenska hraunhella"}, # Guide to lava caves
    {"id": "B0M", "author": "Bragi Ólafsson", "title": "Sendiherrann:ljóð í óbundnu máli"}, # Novel about an ambassador to france (?)
    # (this is already in icepahc) {"id": "B0N", "author": "Einar Kárason", "title": "Ofsi"},
    {"id": "B0O", "author": "Einar Már Guðmundsson", "title": "Rimlar hugans:ástarsaga"}, # Fictional love story told through letters
    {"id": "B0P", "author": "Elín Vilhelmsdóttir", "title": "Lesblinda:dyslexia, fróðleikur og ráðgjöf"}, # Book on handling dyslexia
    {"id": "B0Q", "author": "Elías Snæland Jónsson", "title": "Valkyrjan"}, # Children's book (fiction)
    {"id": "B0R", "author": "Elísabet Jökulsdóttir", "title": "Heilræði lásasmiðsins"}, # Romance
    {"id": "B0S", "author": "Erla Bolladóttir", "title": "Erla góða, Erla"}, # Biography on Erla
    {"id": "B0T", "author": "Fríða Á. Sigurðardóttir", "title": "Í húsi Júlíu"}, # Novel
    {"id": "B0U", "author": "Gerður Kristný Guðjónsdóttir", "title": "Ballið á Bessastöðum"}, # Children's book (fiction)
    {"id": "B0V", "author": "Gerður Kristný Guðjónsdóttir", "title": "Garðurinn"}, # Young adult fiction
    {"id": "B0W", "author": "Gerður Kristný Guðjónsdóttir", "title": "Myndin af pabba:saga Thelmu"}, # Biography
    {"id": "B0X", "author": "Gísli Gunnarsson", "title": "Fiskurinn sem munkunum þótti bestur:Íslandsskreiðin á framandi slóðum 1600-1800"}, # Nonfiction about icelandic merchants in foreign countries
    {"id": "B0Y", "author": "Gísli Sigurðsson", "title": "Túlkun Íslendingasagna í ljósi munnlegrar hefðar:tilgáta um aðferð"}, # Nonfiction essay on icelandic sagas
    {"id": "B0Z", "author": "Guðjón Ragnar Jónasson", "title": "Með hetjur á heilanum"}, # Children's book
    # (this is already in icepahc) {"id": "B1A", "author": "Guðmundur Andri Thorsson", "title": "Segðu mömmu að mér líði vel:saga um ástir"},
    {"id": "B1B", "author": "Guðmundur Eggertsson", "title": "Líf af lífi:gen, erfðir, erfðatækni"}, # Overview of science behind genes and genetic engineering
    {"id": "B1C", "author": "Guðmundur Pálmason", "title": "Jarðhitabók:eðli og nýting auðlinda"}, # Nonfiction overview of geothermal energy
    {"id": "B1D", "author": "Guðrún Eva Mínervudóttir", "title": "Skaparinn"}, # Novel
    {"id": "B1E", "author": "Guðrún Helgadóttir", "title": "Bara gaman"}, # Children's novel
    {"id": "B1F", "author": "Guðrún Helgadóttir", "title": "Öðruvísi dagar"}, # Children's novel
    {"id": "B1G", "author": "Gunnar Helgi Kristinsson", "title": "Íslenska stjórnkerfið"}, # Nonfiction on icelandic politics
    {"id": "B1H", "author": "Gunnar Hersveinn", "title": "Gæfuspor:gildin í lífinu"}, # Self-help book
    {"id": "B1I", "author": "Gunnar Karlsson", "title": "Inngangur að miðöldum:handbók í íslenskri miðaldasögu"}, # Nonfiction iceland in the middle ages
    {"id": "B1K", "author": "Hallgrímur Helgason", "title": "10 ráð til að hætta að drepa fólk og byrja að vaska upp"}, # Fiction on a croatian guy in iceland
    {"id": "B1L", "author": "Hanna Björg Sigurjónsdóttir", "title": "Ósýnilegar fjölskyldur:seinfærar/þroskaheftar mæður og börn þeirra"}, # Scholarly study on certain types of families
    {"id": "B1N", "author": "Harpa Jónsdóttir", "title": "Ferðin til Samiraka"}, # Children's novel
    {"id": "B1O", "author": "Harpa Njálsdóttir", "title": "Fátækt á Íslandi við upphaf nýrrar aldar:hin dulda félagsgerð borgarsamfélagsins"}, # Nonfiction poverty in iceland
    {"id": "B1P", "author": "Helgi Gunnlaugsson", "title": "Afbrot á Íslandi:greinasafn í afbrotafræði"}, # nonfiction on crime in iceland
    {"id": "B1Q", "author": "Helgi Skúli Kjartansson", "title": "Framtíð handan hafs:Vesturfarir frá Íslandi 1870-1914"}, # nonfiction on migration from iceland to america
    {"id": "B1R", "author": "Hera Karlsdóttir", "title": "Tarot:nútíð og framtíð"}, # guide on reading tarot cards
    {"id": "B1S", "author": "Hermann Óskarsson", "title": "Heilbrigði og samfélag:heilsufélagsfræðilegt sjónarhorn"}, # Nonfiction on health and society
    {"id": "B1T", "author": "Héðinn Svarfdal Björnsson", "title": "Háski og hundakjöt:á vit kínverskra ævintýra"}, # Book on travels in China (unclear if fiction or nonfiction)
    # {"id": "B1U", "author": "Hildur Hákonardóttir", "title": "Ætigarðurinn :handbók grasnytjungsins"}, # book on spending time w/ mother nature, includes recipes and stories and healing stuff (removing because parts are cookbook-like)
    {"id": "B1V", "author": "Hildurn Helgadóttir", "title": "Í felulitum:við friðargæslu í Bosníu með breska hernum"}, # Nonfiction on Iceandic soldiers in Bosnia
    {"id": "B1W", "author": "Hrund Þórsdóttir", "title": "Loforðið"}, # Children's novel
    {"id": "B1X", "author": "Hulda Jensdóttir", "title": "Upphafið:bréf til þín frá ljósunni þinni"}, # Guide to childbirth from a midwife
    {"id": "B1Y", "author": "Iðunn Steinsdóttir", "title": "Snuðra og Tuðra og eyðslupúkinn"}, # Children's novel
    {"id": "B1Z", "author": "Ingi Sigurðsson", "title": "Erlendir straumar og íslenzk viðhorf :áhrif fjölþjóðlegra hugmyndastefna á Íslendinga 1830–1918"}, # nonfiction
    {"id": "B2A", "author": "Ingibjörg Hjartardóttir", "title": "Þriðja bónin:saga móður hans"}, # Novel
    {"id": "B2B", "author": "Ingibjörg Haraldsdóttir", "title": "Veruleiki draumanna:endurminningar"}, # Autobiography
    {"id": "B2C", "author": "Íris Ellenberger", "title": "Íslandskvikmyndir 1916-1966:ímyndir, sjálfsmynd og vald"}, # nonfiction on films in inceland
    {"id": "B2D", "author": "Jóhanna Einarsdóttir", "title": "Lítil börn með skólatöskur:tengsl leikskóla og grunnskóla"}, # nonfiction on transition between preschool and elementary school
    {"id": "B2E", "author": "Jón Hallur Stefánsson", "title": "Vargurinn"}, # Novel
    {"id": "B2F", "author": "Jón Hnefill Aðalsteinsson", "title": "&quot;Mannablót&quot;:í Kristnitakan á Íslandi"}, # nonfiction on christianization of iceland
    {"id": "B2G", "author": "Jón Kalmann Stefánsson", "title": "Himnaríki og helvíti"}, # Novel
    {"id": "B2H", "author": "Jón Karl Helgason", "title": "Ferðalok:skýrsla handa akademíu"}, # nonfiction
    {"id": "B2I", "author": "Jón Ólafur Ísberg", "title": "Líf og lækningar:íslensk heilbirgðissaga"}, # nonfiction health in iceland
    {"id": "B2J", "author": "Jón R. Hjálmarsson", "title": "Þjóðkunnir menn við þjóðveginn:frá landnámi til lýðveldis"}, # prose (novel?)
    {"id": "B2K", "author": "Jónas Kristjánsson", "title": "Landnámsmaður Vesturheims:Vínlandsför Þorfinns karlsefnis"}, # nonfiction on first icelandic settlers in vinland
    {"id": "B2L", "author": "Kristín Björnsdóttir", "title": "Líkami og sál:hugmyndir, þekking og aðferðir í hjúkrun"}, # nonfiction on history of modern nursing
    {"id": "B2M", "author": "Kristín Steinsdóttir", "title": "Á eigin vegum"}, # Novel
    {"id": "B2N", "author": "Kristín Steinsdóttir", "title": "Sólin sest að morgni"}, # Novel
    {"id": "B2O", "author": "Lára Magnúsardóttir", "title": "Bannfæring og kirkjuvald á Íslandi 1275-1550:Lög og rannsóknarforsendur"}, # Nonficton
    {"id": "B2P", "author": "Matthías Johannessen", "title": "Málsvörn og minningar"}, # sortof autobiographical nonfiction?
    {"id": "B2Q", "author": "Oddný Eir Ævarsdóttir", "title": "Opnun kryppunnar:brúðuleikhús"}, # novel
    {"id": "B2R", "author": "Ólafur Gunnarsson", "title": "Öxin og jörðin:söguleg skáldsaga um Jón biskup Arason og syni hans"}, # historical novel
    {"id": "B2S", "author": "Ólafur Jóhann Ólafsson", "title": "Aldingarðurinn"}, # 12 short stories
    {"id": "B2T", "author": "Páll Rúnar Elísson", "title": "Breiðarvíkurdrengur:brotasaga Páls Rúnars Elísonar"}, # Autobiography
    {"id": "B2U", "author": "Páll Sigurðsson", "title": "Lagaslóðir:Greinar um lög og rétt"}, # 13 essays on legal topics
    {"id": "B2V", "author": "Pétur Gunnarsson", "title": "ÞÞ í fátæktarlandi:þroskasaga Þórbergs Þórðarsonar"}, # biography
    {"id": "B2W", "author": "Pétur Halldórsson", "title": "Stærð veraldar"}, # nonfiction about astrology (?)
    {"id": "B2X", "author": "Ragnar Arnalds", "title": "Eldhuginn - sagan um Jörund hundadagakonung og byltingu hans á Íslandi:söguleg skáldsaga"}, # a historical novel
    {"id": "B2Y", "author": "Ragnar Gíslason", "title": "Setuliðið"}, # Novel
    {"id": "B2Z", "author": "Reynir Traustason", "title": "Ljósið í djúpinu:örlagasaga Rögnu Aðalsteinsdóttur á Laugabóli"}, # Biography
    {"id": "B3A", "author": "Róbert Jack", "title": "Hversdagsheimspeki:upphafi og endurvakning"}, # Nonfiction on philosophy, history of socratic dialogue
    {"id": "B3B", "author": "Rósa Eggertsdóttir", "title": "Lexía:fræði um leshömlun, kenningar og mat"}, # Nonfiction on dyslexia (?)
    {"id": "B3C", "author": "Sigmundur Ernir Rúnarsson", "title": "Barn að eilífu:ég hélt ég hefði eignast heilbrigt barn, á átján árum hvarf það inn í óþekktan sjúkdóm"}, # novel (?)
    {"id": "B3D", "author": "Sigríður Dúna Kristmundsdóttir", "title": "Ólafía:ævisaga Ólafíu Jóhannsdóttur"}, # Biography
    # {"id": "B3E", "author": "Sigríður Gunnarsdóttir", "title": "Sælkeraferð um Frakkland :135 uppskriftir að hamingjunni á franska vísu / eldaðar af Sigríði Gunnarsdóttur ; myndaðar af Silju Sallé"}, # Cookbook
    {"id": "B3F", "author": "Sigrún Davíðsdóttir", "title": "Feimnismál"}, # Novel
    {"id": "B3G", "author": "Sigrún Helgadóttir", "title": "Jökulsárgljúfur:Dettifoss, Ásbyrgi og allt þar á milli"}, # Geographical description of part of iceland
    {"id": "B3H", "author": "Sigurður A. Magnússon", "title": "Garður guðsmóður:munkríkið Aþos - elsta lýðveldi í heimi"}, # Nonfiction
    {"id": "B3I", "author": "Sigurjón Magnússon", "title": "Gaddavír"}, # Novel
    {"id": "B3J", "author": "Sindri Freysson", "title": "Flóttinn"}, # Novel
    {"id": "B3K", "author": "Símon Jón Jóhannsson", "title": "Spádómabókin"}, # Nonfiction on methods to predict the future
    {"id": "B3L", "author": "Skúli Magnússon", "title": "Hin lagalega aðferð og réttarheimildirnar:fimm ritgerðir í almennri lögfræði og réttarheimspeki"}, # Five essays on legal topics
    {"id": "B3M", "author": "Sólveig Anna Bóasdóttir", "title": "Ást, kynlíf og hjónaband"}, # Discussion of love, sex, and marriage in modern day
    # {"id": "B3N", "author": "Stefanía Valdís Stefánsdóttir", "title": "Eldað í dagsins önn:fljótlegir og hollir heimilisréttir"}, # Cookbook
    {"id": "B3O", "author": "Steingrímur J. Sigfússon", "title": "Við öll:íslenskt velferðarsamfélag á tímamótum"}, # Nonfiction on iceland's welfare state
    {"id": "B3P", "author": "Steinunn Jóhannesdóttir", "title": "Reisubók Guðríðar Símonardóttur:skáldsaga byggð á heimildum"}, # Historical Novel
    {"id": "B3Q", "author": "Steinar Bragi", "title": "Konur"}, # Novel
    {"id": "B3R", "author": "Steinunn Sigurðardóttir", "title": "Hundrað dyr í golunni"}, # Novel
    {"id": "B3S", "author": "Súsanna Svavarsdóttir", "title": "Diddú"}, # Autobiography
    {"id": "B3T", "author": "Thomas Möller", "title": "Eldaðu maður"}, # Cookbook (for men)
    {"id": "B3U", "author": "Unnur Jökulsdóttir", "title": "Hefurðu séð huldufólk:ferðasaga"}, # Nonfiction on "hidden people"
    {"id": "B3V", "author": "Úlfar Hauksson", "title": "Gert út frá Brussel?: sjávarútvegsstefna ESB rannsökuð út frá hugsanlegri aðild Íslands að sambandinu"}, # Nonfiction on joining EU
    {"id": "B3W", "author": "Úlfar Þormóðsson", "title": "Rauð mold:skáldsaga um Íslendinga í Barbaríu"}, # Historical Novel on Turkish raid
    {"id": "B3X", "author": "Vésteinn Ólason", "title": "Ég tek það gilt:greinar um íslenskar bókmenntir á 20. öld"}, # Essays on literature
    {"id": "B3Y", "author": "Viktor Arnar Ingólfsson", "title": "Afturelding"}, # Novel
    {"id": "B3Z", "author": "Þorbjörn Broddason", "title": "Ritlist, prentlist, nýmiðlar"}, # Nonfiction on writing, printing, new media
    {"id": "B4A", "author": "Þorgrímur Þráinsson", "title": "Þriðju ísbjörninn"}, # Children's novel
    {"id": "B4B", "author": "Þorvaldur Gylfason", "title": "Framtíðin er annað land"}, # Essays on Economics
    {"id": "B4C", "author": "Þórarinn Eldjárn", "title": "Baróninn:skáldsaga"}, # Historical Novel on a french baron
    {"id": "B4D", "author": "Þórhallur Heimisson", "title": "Hjónaband og sambúð:leiðir til að efla ást, vináttu og hamingju"}, # Marriage help book
    {"id": "B4E", "author": "Þórunn Hrefna Sigurjónsdóttir", "title": "Ég skal vera grýla:Margrét Pála Ólafsdóttir í lífsspjalli"}, # Biography
    {"id": "B4F", "author": "Þráinn Bertelsson", "title": "Englar dauðans"}, # Novel
    {"id": "B4H", "author": "Þröstur Helgason", "title": "Einkavegir"}, # Collection of articles
    {"id": "B4I", "author": "--------", "title": "Hlutabréf og eignastýring:að velja hlutabréf og byggja upp eignir"}, # Guide to investing
    {"id": "B4J", "author": "Árni Johnsen", "title": "Lífsins melódí"}, # Short story collection
    {"id": "B4K", "author": "Eyvindur Karlsson", "title": "Ósagt"}, # Novel
    {"id": "B4L", "author": "Vigdís Grímsdóttir", "title": "Þegar stjarna hrapar"}, # Novel
    {"id": "B4M", "author": "Stefán Máni", "title": "Skipið"}, # Novel
    {"id": "B4N", "author": "Steinunn Sigurðardóttir", "title": "Sólskinshestur"}, # Novel
    {"id": "B4O", "author": "Þorleifur Friðriksson", "title": "Við brún nýs dags:saga Verkamannafélagsins Dagsbrúnar 1906-1930"}, # Nonfiction historical
    {"id": "B4P", "author": "Sigurður A. Magnússon", "title": "Á hnífsins egg:átakasaga"}, # Autobiography
    {"id": "B4Q", "author": "Sigurjón Árni Eyjólfsson", "title": "Tilvist, trú og tilgangur"}, # Book on Theology
    {"id": "B4R", "author": "Rannveig Traustadóttir", "title": "Fötlun:hugmyndir og aðferðir á nýju fræðasviði: Inngangur: Skipta fræðin máli"}, # Essay
    {"id": "B4S", "author": "Rannveig Traustadóttir", "title": "Fötlun:hugmyndir og aðferðir á nýju fræðasviði: 1. Í nýjum fræðaheimi: Upphaf fötlunarfræða og átök ólíkra hugmynda"}, # Essay
    {"id": "B4T", "author": "Rannveig Traustadóttir", "title": "Fötlun:hugmyndir og aðferðir á nýju fræðasviði: 4. Frá umbótarannsóknum til fræðilegrar fágunar: Þróun fötlunarrannsókna á Norðurlöndum"}, # Essay
    {"id": "B4U", "author": "Rannveig Traustadóttir", "title": "Fötlun:hugmyndir og aðferðir á nýju fræðasviði: 10. Fötlunarrannsóknir: Áherslur og álitamál í rannsóknum með fötluðu fólki"}, # Essay
    {"id": "B4V", "author": "Rannveig Traustadóttir", "title": "Fötlunarfræði:nýjar íslenskar rannsóknir: Inngangur: Fötlun, fræði og samfélag"}, # Essay
    {"id": "B4W", "author": "Rannveig Traustadóttir", "title": "Fötlunarfræði:nýjar íslenskar rannsóknir: Fötlunarfræði: Sjónarhorn, áherslur og aðferðir á nýju fræðasviði"}, # Essay
    {"id": "B4X", "author": "Hanna Björg Sigurjónsdóttir", "title": "Fötlun:hugmyndir og aðferðir á nýju fræðasviði: 3. Valdefling: Glíma við margrætt hugtak"}, # Essay
    {"id": "B4Y", "author": "Hanna Björg Sigurjónsdóttir", "title": "Fötlun:hugmyndir og aðferðir á nýju fræðasviði: 6. Völd og valdaleysi: Um siðferði og ábyrgð rannsakanda"}, # Essay
    {"id": "B5S", "author": "Huldar Breiðfjörð", "title": "Færeyskur dansur:ferðalýsing"}, # Nonfiction
    {"id": "B5T", "author": "Bergsveinn Birgisson", "title": "Handbók um hugarfar kúa:skáldfræðisaga"}, # Novel
    {"id": "B5U", "author": "Hildur Hákonardóttir", "title": "Já, ég þori, get og vil:kvennafrídagurinn 1975, Vilborg Harðardóttir og allar konurnar sem bjuggu hann til"}, # History of women's movement in Iceland
    # {"id": "B5V", "author": "Nanna Rögnvaldsdóttir", "title": "Maturinn okkar:sígildir íslenskir réttir"}, # Cookbook
    {"id": "B5W", "author": "Pétur H. Ármannson", "title": "Landsvirkjun 1965-2005:fyrirtækið og umhverfi þess: Orkuver og arkitektúr"}, # History
    {"id": "B5X", "author": "Sigrún Pálsdóttir", "title": "Landsvirkjun 1965-2005:fyrirtækið og umhverfi þess: Inngangur"}, # History
    {"id": "B5Y", "author": "Sigrún Pálsdóttir", "title": "Landsvirkjun 1965-2005:fyrirtækið og umhverfi þess: Landsvirkjun: fyrirtækið, framkvæmdir þess og hlutverk"}, # History
    # Many of these by Baldur Jónsson appear to be from mbl.is
    # {"id": "J05", "author": "Baldur Jónsson", "title": "Gísli Jónsson, kveðjuorð"}, # Eulogy?
    # {"id": "J06", "author": "Baldur Jónsson", "title": "Hornfirska vegin og metin"}, # Article
    # {"id": "J07", "author": "Baldur Jónsson", "title": "Hreinn Benediktsson, minning"}, # Eulogy?
    # {"id": "J08", "author": "Baldur Jónsson", "title": "Fiðrildin og duggan"}, # Article
    # {"id": "J09", "author": "Baldur Jónsson", "title": "Látra-Björg á Hrafnagili"}, # ??
    # {"id": "J10", "author": "Baldur Jónsson", "title": "Þættir úr sögu Hvassafellsættar"}, # Article
    # {"id": "J11", "author": "Baldur Jónsson", "title": "Lítið eitt um tölvutækniorð - að gefnu tilefni"}, # Article
    # {"id": "J12", "author": "Baldur Jónsson", "title": "Skothent innrím frá Krossanesi"}, # ??
    # {"id": "J13", "author": "Baldur Jónsson", "title": "Ráðunautur í eignarfalli"}, # Article
    # {"id": "J14", "author": "Baldur Jónsson", "title": "Gunnlaugur P. Kristinsson - Minning"}, # Eulogy
    # {"id": "J15", "author": "Baldur Jónsson", "title": "Spjallað við Hitler"}, # Article
    # {"id": "J16", "author": "Baldur Jónsson", "title": "Hvers vegna er bragð að matnum?"}, # Article
    # {"id": "J18", "author": "Baldur Jónsson", "title": "Um bragðið að matnum"}, # Article
    # {"id": "J19", "author": "Baldur Jónsson", "title": "Baldur Ingimarsson - Minning"}, # Eulogy?
    # {"id": "J20", "author": "Baldur Jónsson", "title": "Orð til umhugsunar"}, # Article?
    # {"id": "J21", "author": "Baldur Jónsson", "title": "Á flakki með Látra-Björgu"}, # Article?
    # {"id": "J22", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Formáli"},
    # {"id": "J23", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur"}, # Introduction
    # {"id": "J24", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Ágrip af ræðu áhrærandi íslenskuna\" eftir Konráð Gíslason.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J25", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að bókafregn eftir Konráð Gíslason sem birtist í Fjölni, 7. árg. (1844), bls. 71-104."}, # Essay Introduction
    # {"id": "J26", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Um móðurmálið\" eftir Þórð Jónsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J27", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Hugmynd fyrir sig\" eftir Sveinbjörn Hallgrímsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J28", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Um mál vort Íslendinga I-II\" eftir Jón Guðmundsson.  Æviágrip höfundar og inngangur um ritgerðir."}, # Essay Introduction
    # {"id": "J29", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Alþing og alþingismál (Brot)\" eftir Jón Sigurðsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J30", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Kafli úr bréfi\" eftir Pál Melsteð.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J31", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Íslensk orðmyndan\" eftir Einar Benediktsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J32", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Móðurmálið\" eftir Guðmund Björnson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J34", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Móðurmálið\" eftir Guðmund Finnbogason.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J35", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Hreint mál\" eftir Guðmund Finnbogason."}, # Essay Introduction
    # {"id": "J36", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Ættarnöfn\" eftir Guðmundur Kamban.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J38", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Tungan\" eftir Benedikt Jónsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J39", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Um ættarnöfn\" eftir Árna Pálsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J40", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Um ættarnöfn\" eftir Árna Pálsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J41", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Málfrelsi\" eftir Sigurð Nordal.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
    # {"id": "J42", "author": "Baldur Jónsson", "title": "Þjóð og tunga:RITGERÐIR OG RÆÐUR FRÁ TÍMA SJÁLFSTÆÐISBARÁTTUNNAR: Inngangur að ritgerðinni \"Þróun íslenskunnar\" eftir Kristján Albertsson.  Æviágrip höfundar og inngangur um ritgerð."}, # Essay Introduction
]
