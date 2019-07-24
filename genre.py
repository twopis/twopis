# This file contains a variety of dictionaries converting from author names
# to features like the century written, genre, dialect, etc.
# This is obviously a lot of data, so it may not be completely perfect,
# but I tried my best and based it on other sources where possible.
import numpy as np

# This can get a little tricky as authors write over a range of times,
# not in century increments. I've tried my best to pick the century
# where the author was most active, recognizing that this means an author
# writing from 1880-1905 and an author writing from 1895-1910 are
# "writing in different centuries". For this analysis, we are looking at long
# timescales, so the hope is one century won't be a huge issue. Future work
# would have to put a timestamp on when each individual segment was composed
# (itself a little tricky) and somehow make more accurate guesses for ancient
# authors writing in a wider range.
namesToCent = {
    "AchillesTatius": 2,
    "Aelian": 3,
    "AeneasTacticus": -4,
    "Aeschines": -4,
    "Aeschylus": -5,
    "Andocides": -5,
    "Antiphon": -5,
    "PseudoApollodorus": 2,
    "ApolloniusRhodius": -3,
    "Appian": 2,
    "AratusSolensis": -3,
    "Aretaeus": 1,
    "AeliusAristides": 2,
    "Aristophanes": -5,
    "Aristotle": -4,
    "Arrian": 2,
    "Asclepiodotus": -1,
    "Athenaeus": 3,
    "MarcusAurelius": 2,
    "Bacchylides": -5,
    "Barnabas": 1,
    "BasilBishopOfCaesarea": 4,
    "BionOfPhlossa": -2,
    "Callimachus": -3,
    "Callistratus": 3,
    "Chariton": 1,
    "ClementOfAlexandria": 3,
    "Colluthus": 6,
    "Demades": -4,
    "DemetriusOfPhaleron": -3,
    "Demosthenes": -4,
    "Dinarchus": -4,
    "DioChrysostom": 2,
    "CassiusDio": 3,
    "DiodorusSiculus": -1,
    "DiogenesLaertius": 3,
    "DionysiusOfHalicarnassus": -1,
    "Epictetus": 2,
    "Euclid": -4,
    "Euripides": -5,
    "EusebiusOfCaesarea": 4,
    "Galen": 3,
    "ValeriusHarpocration": 2,
    "Herodotus": -5,
    "Hesiod": -8,
    "Hippocrates": -5,
    "Homer": -8,
    "Anonymous(Hymns_Dionysus)": -8,
    "Anonymous(Hymns_Demeter)": -8,
    "Anonymous(Hymns_Apollo)": -8,
    "Anonymous(Hymns_Hermes)": -2, #??
    "Anonymous(Hymns_Aphrodite)": -8,
    "Anonymous(Hymns_Rest)": -2, #??
    "Hyperides": -4,
    "Isaeus": -4,
    "Isocrates": -4,
    "JohnOfDamascus": 8,
    "FlaviusJosephus": 1,
    "Longinus": 1,
    "Longus": 2,
    "Lucian": 2,
    "Lycophron": -3,
    "Lycurgus": -4,
    "Lysias": -4,
    "Moschus": -2,
    "Anon_Bios": -1,
    "Anon_Megara": -1,
    "Bible": 1,
    "Nonnus": 5,
    "Onasander": 1,
    "OppianOfApamea": 2,
    "Oppian": 3,
    "Parthenius": -1,
    "Pausanias": 2,
    "PhilostratusTheAthenian": 3,
    "PhilostratusMinor": 3,
    "PhilostratusTheLemnian": 3,
    "Pindar": -5,
    "Plato": -4,
    "Plutarch": 2,
    "Polybius": -2,
    "Procopius": 6,
    "PseudoPlutarch": 3,
    "PseudoXenophon": -5,
    "ClaudiusPtolemy": 2,
    "QuintusSmyrnaeus": 4,
    "Sophocles": -5,
    "Strabo": 1,
    "Theocritus": -3,
    "Theophrastus": -3,
    "Thucydides": -5,
    "Tryphiodorus": 3,
    "XenophonOfEphesus": 3,
    "Xenophon": -4,
    "Abraham_Lincoln": 19,
    "Agatha_Christie": 20,
    "Albert_Einstein": 20,
    "Aldous_Huxley": 20,
    "Alexander_Pope": 18,
    "Alfred_Russel_Wallace": 19,
    "Ambrose_Bierce": 19,
    "Andrew_Lang": 19,
    "Anthony_Trollope": 19,
    "Arnold_Joseph_Toynbee": 20,
    "Baronness_Orczy": 20, # started 1899, so i'll list as 20th
    "Beatrix_Potter": 20, # started late 1890s, so i'll lista s 20th
    "Benjamin_Disraeli": 19,
    "Benjamin_Franklin": 18,
    "Bertrand_Russell": 20,
    "Bram_Stoker": 19,
    "Bret_Harte": 19,
    "Charles_Darwin": 19,
    "Charles_Dickens": 19,
    "Charles_Kingsley": 19,
    "Charlotte_Bronte": 19,
    "Charlotte_Mary_Yonge": 19,
    "D_H_Lawrence": 20,
    "Daniel_Defoe": 18,
    "Edgar_Allan_Poe": 19,
    "Edgar_Rice_Burroughs": 20,
    "Edmund_Burke": 18,
    "Edward_Phillips_Oppenheim": 20, # majority in 1900s
    "Edward_Stratemeyer": 20,
    "Elizabeth_Barrett_Browning": 19,
    "Emily_Bronte": 19,
    "Eugene_O_Neill": 20,
    "Ezra_Pound": 20,
    "Frank_Richard_Stockton": 19,
    "G_K_Chesterton": 20,
    "George_Alfred_Henty": 19,
    "George_Bernard_Shaw": 19,
    "George_Eliot": 19,
    "George_Washington": 18,
    "Grant_Allen": 19,
    "Hamlin_Garland": 20, # some late 19, but mostly early 20
    "Harold_Bindloss": 20,
    "Harriet_Elizabeth_Beecher_Stowe": 19,
    "Hector_Hugh_Munro": 20,
    "Henry_David_Thoreau": 19,
    "Henry_Francis_Cary": 19,
    "Henry_James": 19, # some early 20 stuff
    "Henry_Rider_Haggard": 19, # some early 20
    "Herbert_George_Wells": 20, # mostly 20
    "Herbert_Spencer": 19,
    "Herman_Melville": 19,
    "Howard_Pyle": 19,
    "Isaac_Asimov": 20,
    "Jack_London": 20, # some late 1890s stuff
    "Jacob_Abbott": 19,
    "James_Bowker": 20,
    "James_Fenimore_Cooper": 19,
    "James_Joyce": 20,
    "James_Matthew_Barrie": 20, #???
    "James_Otis": 20, # really on the border, both late 19 and early 20
    "James_Russell_Lowell": 19,
    "Jane_Austen": 19,
    "Jerome_Klapka_Jerome": 19, # late 19 though
    "John_Bunyan": 17,
    "John_Dryden": 17,
    "John_Galsworthy": 20,
    "John_Keats": 19,
    "John_Locke": 17,
    "John_Maynard_Keynes": 20,
    "John_Milton": 17,
    "John_Morley": 19,
    "John_Ruskin": 19,
    "John_Stuart_Mill": 19,
    "Jonathan_Swift": 18,
    "Joseph_Conrad": 20, # late 19, but lots of early 20
    "Leigh_Hunt": 19,
    "Lewis_Carroll": 19,
    "Lord_Byron": 19,
    "Lord_Tennyson": 19,
    "Louisa_May_Alcott": 19,
    "Lucy_Maud_Montgomery": 20,
    "Lyman_Frank_Baum": 20, #some late 19
    "Mark_Twain": 19,
    "Mary_Shelley": 19,
    "Mary_Stewart_Daggett": 20, # one 1911, one 1895....
    "Michael_Faraday": 19,
    "Nathaniel_Hawthorne": 19,
    "O_Henry": 20,
    "Oscar_Wilde": 19,
    "P_B_Shelley": 19,
    "P_G_Wodehouse": 20,
    "Percival_Lowell": 19,
    "Philip_Kindred_Dick": 20,
    "R_M_Ballantyne": 19,
    "Rafael_Sabatini": 20,
    "Ralph_Waldo_Emerson": 19,
    "Richard_Brinsley_Sheridan": 18,
    "Robert_Browning": 19,
    "Robert_Burns": 18,
    "Robert_Frost": 20,
    "Robert_Hooke": 17,
    "Robert_Louis_Stevenson": 19,
    "Robert_Southey": 19,
    "Rudyard_Kipling": 19, # main stuff is late 1800
    "Samuel_Taylor_Coleridge": 18, # late 1700s
    "Sinclair_Lewis": 20,
    "Sir_Arthur_Conan_Doyle": 19, # argh this spans late 1800s, early 1900s
    "Sir_Francis_Galton": 19,
    "Sir_Humphry_Davy": 19,
    "Sir_Isaac_Newton": 18,
    "Sir_Joseph_Dalton_Hooker": 19,
    "Sir_Richard_Francis_Burton": 19,
    "Sir_Walter_Scott": 19,
    "Sir_William_Schwenck_Gilbert": 19,
    "Sir_Winston_Churchill": 20,
    "Stephen_Leacock": 20,
    "T_S_Eliot": 20,
    "Thomas_Carlyle": 19,
    "Thomas_Crofton_Croker": 19,
    "Thomas_Hardy": 19,
    "Thomas_Henry_Huxley": 19,
    "Thomas_Robert_Malthus": 19,
    "Thornton_Waldo_Burgess": 20,
    "Ulysses_Grant": 19,
    "Virginia_Woolf": 20,
    "Walt_Whitman": 19,
    "Walter_de_la_Mare": 20,
    "Washington_Irving": 19,
    "Wilkie_Collins": 19,
    "William_Blake": 19, #...?
    "William_Butler_Yeats": 20, # majority after 1900
    "William_Dean_Howells": 19, # majority before 1900
    "William_Ewart_Gladstone": 19,
    "William_Henry_Hudson": 20, # majority after 1900
    "William_J_Long": 20,
    "William_Makepeace_Thackeray": 19,
    "William_Penn": 19,
    "William_Somerset_Maugham": 20,
    "William_Wordsworth": 19, # some late 1790s, but
    "William_Wymark_Jacobs": 20, #??? late 19 also
    "Winston_Churchill": 20,
    "Zane_Grey": 20,
    "Shakespeare": 16,
    "Chaucer": 14,
    "Anon_(Prik_of_Conscience)": 14,
    "George_Ashby": 15,
    "Gavin_Douglas": 16, # 1500 or 1501
    "John_Audelay": 15,
    "John_Capgrave": 15,
    "John_Gower": 14,
    "John_Hardyng": 15,
    "John_Lydgate": 15,
    "John_Mandeville": 14,
    "John_Metham": 15,
    "John_Mirk": 15,
    "Julian_of_Norwich": 14,
    "Laurence_Minot": 14,
    "Margery_Kempe": 15,
    "Osbern_Bokenham": 15,
    "Robert_Henryson": 15,
    "Thomas_Hoccleve": 15,
    "Thomas_Usk": 14, # Corrupt and questionable date
    "Thomas_Mallory": 15,
    "Walter_Hilton": 14,
    "William_Caxton": 15,
    "William_Dunbar": 16, # and 15
    "William_Paris": 14,
    "Anon_Árna": 14,
    "Anon_Bandamanna_K": 15,
    "Anon_Bandamanna_M": 14,
    "Anon_Ectors": 15,
    "Anon_Finnboga": 14,
    "Anon_Grágás": 13,
    "Anon_Grettis": 14,
    "Anon_Gunnars": 15,
    "Anon_Hómilíubók": 12,
    "Anon_Illuga": 17,
    "Anon_Jarlmanns": 15,
    "Anon_Jarteinabók": 13,
    "Anon_Jómsvíkinga": 13,
    "Anon_Júditarbók": 15,
    "Anon_Miðaldaævintýri": 15,
    "Anon_Morkinskinna": 13,
    "Anon_Mörtu": 14,
    "Anon_Sögu-þáttur": 17,
    "Anon_Vilhjálms": 15,
    "Anon_Víglundar": 15,
    "Anon_Þorláks": 13,
    "Arngrímur_Jónsson": 16,
    "Benedikt_Gröndal": 19,
    "Björn_Þorleifsson": 16,
    "Brandur_Jónsson": 14,
    "Einar_H_Kvaran": 20,
    "Einar_Kárason": 21,
    "Gestur_Pálsson": 19,
    "Gísli_Konráðsson": 19,
    "Guðmundur_Andri_Thorsson": 21,
    "Guðmundur_Einarsson": 17,
    "Halldór_Þorbergsson": 17,
    "Haraldur_Níelsson": 20,
    "Jón_Halldórsson": 18,
    "Jón_Magnússon": 17,
    "Jón_Oddsson_Hjaltalín": 18,
    "Jón_Ólafsson_Indíafari": 17,
    "Jón_Ólafsson_úr_Grunnavík": 18,
    "Jón_Steingrímsson": 18,
    "Jón_Thoroddsen": 19,
    "Jón_Trausti": 20,
    "Jón_Þorkelsson_Vídalín": 18,
    "Jón_Þorláksson": 17,
    "Jónas_Hallgrímsson": 19,
    "Oddur_Gottskálksson": 16,
    "Ólafur_Egilsson": 17,
    "Pétur_Gunnarsson": 20,
    "Pétur_Pétursson": 19,
    "Snorri_Sturluson": 13,
    "Sturla_Þórðarson": 13,
    "The_First_Grammarian": 12,
    "Torfhildur_Hólm": 19,
    "Þorgils_Gjallandi": 20,
    "Þorlákur_Skúlason": 17,
    "Þorsteinn_Björnsson": 17,
    "Þórarinn_Eldjárn": 20,
    "Anon_F1E": 13,
    "Anon_F01": 14,
    "Anon_F02": 14,
    "Anon_F03": -1, # Bjarnar_saga_Hítdælakappa
    "Anon_F04": 13,
    "Anon_F05": 13,
    "Anon_F06": 13,
    "Anon_F07": 13,
    "Anon_F08": 13,
    "Anon_F09": 14,
    "Anon_F0A": 16, # "about 1500"
    "Anon_F0B": 14, # 1290-1385
    "Anon_F0C": 13,
    "Anon_F0E": 13,
    "Anon_F0D": 13,
    "Anon_F0F": 13,
    "Anon_F0K": 13,
    "Anon_F0G": 13,
    "Anon_F0H": -1, #Grænlendinga_þáttur
    "Anon_F0I": 14,
    "Anon_F0J": 15, # or 16th?
    "Anon_F0L": 13, #?
    "Anon_F0M": 13, #?
    "Anon_F0N": 14,
    "Anon_F0O": -1, # Saga of Hávarður of Ísafjörður
    "Anon_F0P": 13, # but debated
    "Anon_F0Q": 13,
    "Anon_F0R": -1, # Hænsa-Þóris saga
    "Anon_F1D": -1, # Íslendinga þættir
    "Anon_F0T": -1, # Jökuls_þáttur_Búasonar
    "Anon_F0S": 14,
    "Anon_F0U": 13,
    "Anon_F0V": 14,
    "Anon_F0X": 13,
    "Anon_F11": 13,
    "Anon_F0Y": 13,
    "Anon_F12": 13, # "about 1200"
    "Anon_F13": 14,
    "Anon_F14": 14, #?; late
    "Anon_F15": 13,
    "Anon_F16": 13,
    "Anon_F17": 15, # late 14, early 15
    "Anon_F18": 13,
    "Anon_F1A": 14, # c. 1300
    "Anon_F1B": 14,
    "Anon_F19": 14,
    "Anon_F1C": 13,
    "Anon_F1G": 12, # or 13?
    "Anon_F1F": 13, # 12th and 13th
    "Ari_Kristján_Sæmundssen": 21,
    "Arnaldur_Birgir_Konráðsson": 21,
    "Arnaldur_Indriðason": 21,
    "Arnþór_Gunnarsson": 21,
    "Auður_Jónsdóttir": 21,
    "Álfheiður_Steinþórsdóttir": 21,
    "Ármann_Jakobsson": 21,
    "Árni_Bergmann": 21,
    "Árni_Björnsson": 21,
    "Bergþór_Pálsson": 21,
    "Birgitta_Jónsdóttir": 21,
    "Björn_Hróarsson": 21,
    "Bragi_Ólafsson": 21,
    "Einar_Kárason": 21,
    "Einar_Már_Guðmundsson": 21,
    "Elín_Vilhelmsdóttir": 21,
    "Elías_Snæland_Jónsson": 21,
    "Elísabet_Jökulsdóttir": 21,
    "Erla_Bolladóttir": 21,
    "Fríða_Á._Sigurðardóttir": 21,
    "Gerður_Kristný_Guðjónsdóttir": 21,
    "Gísli_Gunnarsson": 21,
    "Gísli_Sigurðsson": 21,
    "Guðjón_Ragnar_Jónasson": 21,
    "Guðmundur_Andri_Thorsson": 21,
    "Guðmundur_Eggertsson": 21,
    "Guðmundur_Pálmason": 21,
    "Guðrún_Eva_Mínervudóttir": 21,
    "Guðrún_Helgadóttir": 21,
    "Guðrún_Helgadóttir": 21,
    "Gunnar_Helgi_Kristinsson": 21,
    "Gunnar_Hersveinn": 21,
    "Gunnar_Karlsson": 21,
    "Hallgrímur_Helgason": 21,
    "Hanna_Björg_Sigurjónsdóttir": 21,
    "Harpa_Jónsdóttir": 21,
    "Harpa_Njálsdóttir": 21,
    "Helgi_Gunnlaugsson": 21,
    "Helgi_Skúli_Kjartansson": 21,
    "Hera_Karlsdóttir": 21,
    "Hermann_Óskarsson": 21,
    "Héðinn_Svarfdal_Björnsson": 21,
    "Hildur_Hákonardóttir": 21,
    "Hildurn_Helgadóttir": 21,
    "Hrund_Þórsdóttir": 21,
    "Hulda_Jensdóttir": 21,
    "Iðunn_Steinsdóttir": 21,
    "Ingi_Sigurðsson": 21,
    "Ingibjörg_Hjartardóttir": 21,
    "Ingibjörg_Haraldsdóttir": 21,
    "Íris_Ellenberger": 21,
    "Jóhanna_Einarsdóttir": 21,
    "Jón_Hallur_Stefánsson": 21,
    "Jón_Hnefill_Aðalsteinsson": 21,
    "Jón_Kalmann_Stefánsson": 21,
    "Jón_Karl_Helgason": 21,
    "Jón_Ólafur_Ísberg": 21,
    "Jón_R._Hjálmarsson": 21,
    "Jónas_Kristjánsson": 21,
    "Kristín_Björnsdóttir": 21,
    "Kristín_Steinsdóttir": 21,
    "Lára_Magnúsardóttir": 21,
    "Matthías_Johannessen": 21,
    "Oddný_Eir_Ævarsdóttir": 21,
    "Ólafur_Gunnarsson": 21,
    "Ólafur_Jóhann_Ólafsson": 21,
    "Páll_Rúnar_Elísson": 21,
    "Páll_Sigurðsson": 21,
    "Pétur_Gunnarsson": 21,
    "Pétur_Halldórsson": 21,
    "Ragnar_Arnalds": 21,
    "Ragnar_Gíslason": 21,
    "Reynir_Traustason": 21,
    "Róbert_Jack": 21,
    "Rósa_Eggertsdóttir": 21,
    "Sigmundur_Ernir_Rúnarsson": 21,
    "Sigríður_Dúna_Kristmundsdóttir": 21,
    "Sigríður_Gunnarsdóttir": 21,
    "Sigrún_Davíðsdóttir": 21,
    "Sigrún_Helgadóttir": 21,
    "Sigurður_A._Magnússon": 21,
    "Sigurjón_Magnússon": 21,
    "Sindri_Freysson": 21,
    "Símon_Jón_Jóhannsson": 21,
    "Skúli_Magnússon": 21,
    "Sólveig_Anna_Bóasdóttir": 21,
    "Stefanía_Valdís_Stefánsdóttir": 21,
    "Steingrímur_J._Sigfússon": 21,
    "Steinunn_Jóhannesdóttir": 21,
    "Steinar_Bragi": 21,
    "Steinunn_Sigurðardóttir": 21,
    "Súsanna_Svavarsdóttir": 21,
    "Thomas_Möller": 21,
    "Unnur_Jökulsdóttir": 21,
    "Úlfar_Hauksson": 21,
    "Úlfar_Þormóðsson": 21,
    "Vésteinn_Ólason": 21,
    "Viktor_Arnar_Ingólfsson": 21,
    "Þorbjörn_Broddason": 21,
    "Þorgrímur_Þráinsson": 21,
    "Þorvaldur_Gylfason": 21,
    "Þórarinn_Eldjárn": 20, # already above from icepahc, but accent misses seem to be an isse
    "Þórhallur_Heimisson": 21,
    "Þórunn_Hrefna_Sigurjónsdóttir": 21,
    "Þráinn_Bertelsson": 21,
    "Þröstur_Helgason": 21,
    "--------": 21,
    "Árni_Johnsen": 21,
    "Eyvindur_Karlsson": 21,
    "Vigdís_Grímsdóttir": 21,
    "Stefán_Máni": 21,
    "Þorleifur_Friðriksson": 21,
    "Sigurjón_Árni_Eyjólfsson": 21,
    "Rannveig_Traustadóttir": 21,
    "Huldar_Breiðfjörð": 21,
    "Bergsveinn_Birgisson": 21,
    "Nanna_Rögnvaldsdóttir": 21,
    "Pétur_H._Ármannson": 21,
    "Sigrún_Pálsdóttir": 21,
    "Baldur_Jónsson": 21,
}
# Maps are followed by this function to remove authors
# Who have addendums on their names.
def toCent(name):
    if name[-2:] == "_2":
        name = name[:-2]

    if name[-6:] == "_Prose":
        name = name[:-6]
    if name[-7:] == "_Poetry":
        name = name[:-7]


    return namesToCent[name]


genreLabels = [
    "Prose", # 0
    "Poetry" # 1
]
namesToGenre = {
    "AchillesTatius": 0,
    "Aelian": 0,
    "AeneasTacticus": 0,
    "Aeschines": 0,
    "Aeschylus": 1,
    "Andocides": 0,
    "Antiphon": 0,
    "PseudoApollodorus": 0,
    "ApolloniusRhodius": 1,
    "Appian": 0,
    "AratusSolensis": 1,
    "Aretaeus": 0,
    "AeliusAristides": 0,
    "Aristophanes": 1,
    "Aristotle": 0,
    "Arrian": 0,
    "Asclepiodotus": 0,
    "Athenaeus": 0,
    "MarcusAurelius": 0,
    "Bacchylides": 1,
    "Barnabas": 0,
    "BasilBishopOfCaesarea": 0,
    "BionOfPhlossa": 1,
    "Callimachus": 1,
    "Callistratus": 0,
    "Chariton": 0,
    "ClementOfAlexandria": 0,
    "Colluthus": 1,
    "Demades": 0,
    "DemetriusOfPhaleron": 0,
    "Demosthenes": 0,
    "Dinarchus": 0,
    "DioChrysostom": 0,
    "CassiusDio": 0,
    "DiodorusSiculus": 0,
    "DiogenesLaertius": 0,
    "DionysiusOfHalicarnassus": 0,
    "Epictetus": 0,
    "Euclid": 0,
    "Euripides": 1,
    "EusebiusOfCaesarea": 0,
    "Galen": 0,
    "ValeriusHarpocration": 0,
    "Herodotus": 0,
    "Hesiod": 1,
    "Hippocrates": 0,
    "Homer": 1,
    "Anonymous(Hymns_Dionysus)": 1,
    "Anonymous(Hymns_Demeter)": 1,
    "Anonymous(Hymns_Apollo)": 1,
    "Anonymous(Hymns_Hermes)": 1,
    "Anonymous(Hymns_Aphrodite)": 1,
    "Anonymous(Hymns_Rest)": 1,
    "Hyperides": 0,
    "Isaeus": 0,
    "Isocrates": 0,
    "JohnOfDamascus": 0,
    "FlaviusJosephus": 0,
    "Longinus": 0,
    "Longus": 0,
    "Lucian": 0,
    "Lycophron": 1,
    "Lycurgus": 0,
    "Lysias": 0,
    "Moschus": 1,
    "Anon_Bios": 1,
    "Anon_Megara": 1,
    "Bible": 0,
    "Nonnus": 1,
    "Onasander": 0,
    "OppianOfApamea": 1,
    "Oppian": 1,
    "Parthenius": 0,
    "Pausanias": 0,
    "PhilostratusTheAthenian": 0,
    "PhilostratusMinor": 0,
    "PhilostratusTheLemnian": 0,
    "Pindar": 1,
    "Plato": 0,
    "Plutarch": 0,
    "Polybius": 0,
    "Procopius": 0,
    "PseudoPlutarch": 0,
    "PseudoXenophon": 0,
    "ClaudiusPtolemy": 0,
    "QuintusSmyrnaeus": 1,
    "Sophocles": 1,
    "Strabo": 0,
    "Theocritus": 1,
    "Theophrastus": 0,
    "Thucydides": 0,
    "Tryphiodorus": 1,
    "XenophonOfEphesus": 0,
    "Xenophon": 0,
    #
    "Abraham_Lincoln": 0, # prose
    "Agatha_Christie": 0, # prose
    "Albert_Einstein": 0, # prose
    "Aldous_Huxley": 0, # Poetry: The Defeat of Youth and other Poems
    "Alexander_Pope": 1, # poetry: The_Poetical_Works_of_Alexander_Pope,_Volume_1, The_Rape_of_the_Lock_and_Other_Poems, Works of Alexander Pope, Volume 1 has some poetry, some prose
    "Alfred_Russel_Wallace": 0,
    "Ambrose_Bierce": 0, # Poetry: Black_Beetles_in_Amber, Shapes_of_Clay ;
    "Andrew_Lang": 0, #   Poetry: A_Collection_of_Ballads, Ballads_in_Blue_China_and_Verses_and_Translations, Ban_and_Arriere_Ban, Grass_of_Parnassus, Helen_of_Troy, New_Collected_Rhymes, Rhymes_a_la_Mode
    "Anthony_Trollope": 0, # prose
    "Arnold_Joseph_Toynbee": 0, # Prose
    "Baronness_Orczy": 0, # Prose
    "Beatrix_Potter": 0, # Prose
    "Benjamin_Disraeli": 0, # Prose
    "Benjamin_Franklin": 0, # Prose
    "Bertrand_Russell": 0, # Prose
    "Bram_Stoker": 0, # Prose
    "Bret_Harte": 0, #  Poetry: Complete_Poetical_Works_of_Bret_Harte, Dickens_in_Camp, East_and_West, Excelsior, Her_Letter_His_Answer_&_Her_Last_Letter
    "Charles_Darwin": 0, # Prose
    "Charles_Dickens": 0, # Poetry: The_Poems_and_Verses_of_Charles_Dickens
    "Charles_Kingsley": 0, # Poetry: Andromeda_and_Other_Poems
    "Charlotte_Bronte": 0, # Prose
    "Charlotte_Mary_Yonge": 0, # Prose
    "D_H_Lawrence": 0, # Poetry: Amores, Bay, Look!_We_Have_Come_Through!, New_Poems, Tortoises
    "Daniel_Defoe": 0, # Poetry: The_True-Born_Englishman
    "Edgar_Allan_Poe": 0, # Poetry: Edgar_Allan_Poe's_Complete_Poetical_Works, The_Works_of_Edgar_Allan_Poe_Volume_1 (parts of 5)
    "Edgar_Rice_Burroughs": 0, # Prose
    "Edmund_Burke": 0, # Prose
    "Edward_Phillips_Oppenheim": 0, # Prose
    "Edward_Stratemeyer": 0, # Prose
    "Elizabeth_Barrett_Browning": 1, # Poetry:   'He_Giveth_His_Beloved_Sleep', Sonnets_from_the_Portuguese, The_Poetical_Works_of_Elizabeth_Barrett_Browning_Volume_I
    "Emily_Bronte": 0, # Prose
    "Eugene_O_Neill": 0, # Prose
    "Ezra_Pound": 1, # Poetry: Hugh_Selwyn_Mauberly
    "Frank_Richard_Stockton": 0, # Prose
    "G_K_Chesterton": 0, #   Greybeards_at_Play, Poems, The_Ballad_of_St._Barbara, The_Ballad_of_the_White_Horse, The_Wild_Knight_and_Other_Poems, Wine,_Water,_and_Song
    "George_Alfred_Henty": 0, # Prose
    "George_Bernard_Shaw": 0, # Poetry: The_Admirable_Bashville
    "George_Eliot": 0, # Prose
    "George_Washington": 0, # Prose
    "Grant_Allen": 0, # Prose
    "Hamlin_Garland": 0, # Prose
    "Harold_Bindloss": 0, # Prose
    "Harriet_Elizabeth_Beecher_Stowe": 0, # Prose
    "Hector_Hugh_Munro": 0, # Prose
    "Henry_David_Thoreau": 0, # Prose
    "Henry_Francis_Cary": 0, # Prose
    "Henry_James": 0, # Prose
    "Henry_Rider_Haggard": 0, # Prose
    "Herbert_George_Wells": 0, # Prose
    "Herbert_Spencer": 0, # Prose
    "Herman_Melville": 0, # Poetry: Battle-Pieces_and_Aspects_of_the_War, John_Marr_and_Other_Poems
    "Howard_Pyle": 0, # Prose
    "Isaac_Asimov": 0, # Prose
    "Jack_London": 0, # Prose
    "Jacob_Abbott": 0, # Prose
    "James_Bowker": 0, # Prose
    "James_Fenimore_Cooper": 0, # Prose
    "James_Joyce": 0, # Poetry Chamber_Music
    "James_Matthew_Barrie": 0, # Prose
    "James_Otis": 0, # Prose
    "James_Russell_Lowell": 0, # Poetry: Poems_of_James_Russell_Lowell, The_Complete_Poetical_Works_of_James_Russell_Lowell, The_Vision_of_Sir_Launfal_And_Other_Poems,_Version_1, The_Vision_of_Sir_Launfal_And_Other_Poems,_Version_2
    "Jane_Austen": 0, # Prose
    "Jerome_Klapka_Jerome": 0, # Prose
    "John_Bunyan": 0, # Prose
    "John_Dryden": 0, # Poetry: Dryden's_Works_Vol._2_(of_18) (part of 2, part of 3, 4, part of 5, 7), Palamon_and_Arcite, The_Poetical_Works_of_John_Dryden,_Volume_1 (both volumes)
    "John_Galsworthy": 0, # Prose
    "John_Keats": 1, # Poetry: Endymion, Keats:_Poems_Published_in_1820, Lamia, Poems_1817
    "John_Locke": 0, # Prose
    "John_Maynard_Keynes": 0, # Prose
    "John_Milton": 1, # Poetry:   L'Allegro,_Il_Penseroso,_Comus,_and_Lycidas, Milton's_Comus, Minor_Poems_by_Milton, Paradise_Lost, Paradise_Regained, The_Poetical_Works_of_John_Milton # Comus is mostly footnotes and introduction though
    "John_Morley": 0, # Prose
    "John_Ruskin": 0, # Prose
    "John_Stuart_Mill": 0, # Prose
    "Jonathan_Swift": 0, # Poetry: The_Battle_of_the_Books, The_Poems_of_Jonathan_Swift,_D.D.,_Volume_1
    "Joseph_Conrad": 0, # Prose
    "Leigh_Hunt": 1, # Poetry: Captain_Sword_and_Captain_Pen
    "Lewis_Carroll": 0, # Poetry:   Phantasmagoria_and_Other_Poems, Rhyme?_And_Reason, Songs_From_Alice_in_Wonderland_and_Through_the_Looking-Glass, The_Hunting_of_the_Snark, Three_Sunsets_and_Other_Poems
    "Lord_Byron": 1, # All Poetry
    "Lord_Tennyson": 1, # All Poetry
    "Louisa_May_Alcott": 0, # Poetry: Three_Unpublished_Poems
    "Lucy_Maud_Montgomery": 0, # Prose
    "Lyman_Frank_Baum": 0, # Prose
    "Mark_Twain": 0, # Prose
    "Mary_Shelley": 0, # Poetry: Proserpine_and_Midas
    "Mary_Stewart_Daggett": 0, # Prose
    "Michael_Faraday": 0, # Prose
    "Nathaniel_Hawthorne": 0, # Prose
    "O_Henry": 0, # Prose
    "Oscar_Wilde": 0, # Poetry: Charmides_and_Other_Poems, Poems, Selected_Poems_of_Oscar_Wilde, The_Ballad_of_Reading_Gaol
    "P_B_Shelley": 1, # Poetry:   Adonais, Peter_Bell_the_Third, The_Complete_Poetical_Works_of_Percy_Bysshe_Shelley, The_Daemon_of_the_World, The_Witch_of_Atlas
    "P_G_Wodehouse": 0, # Prose
    "Percival_Lowell": 0, # Prose
    "Philip_Kindred_Dick": 0, # Prose
    "R_M_Ballantyne": 0, # Prose
    "Rafael_Sabatini": 0, # Prose
    "Ralph_Waldo_Emerson": 0, # Poetry: May-Day, Poems
    "Richard_Brinsley_Sheridan": 0, # Poetry: part of The_Duenna
    "Robert_Browning": 1, # All Poetry (selections may have tiny bits of prose)
    "Robert_Burns": 1, # Poems_And_Songs_Of_Robert_Burns, Tam_O'Shanter
    "Robert_Frost": 1, # All Poetry
    "Robert_Hooke": 0, # Prose
    "Robert_Louis_Stevenson": 0, # Poetry   A_Child's_Garden_of_Verses,_Verse_130, A_Child's_Garden_of_Verses,_Verse_142, A_Child's_Garden_of_Verses,_Verse_154, A_Child's_Garden_of_Verses,_Verse_158, A_Child's_Garden_of_Verses,_Version_1, A_Child's_Garden_of_Verses,_Version_2, A_Child's_Garden_of_Verses,_Version_3, A_Child's_Garden_of_Verses,_Version_4, A_Lowden_Sabbath_Morn, Ballads, Moral_Emblems, New_Poems, Prayers_Written_At_Vailima, Songs_of_Travel, The_Works_of_Robert_Louis_Stevenson_-_Swanston_Edition,_Volume_1 (14, Some in 22), Underwoods
    "Robert_Southey": 1, # Poetry: Poems,_1799, Poems
    "Rudyard_Kipling": 0, # Poetry: A_Song_of_the_English, An_Almanac_of_Twelve_Sports, Barrack-Room_Ballads, Departmental_Ditties_and_Barrack_Room_Ballads, Kipling_Stories_and_Poems_Every_Child_Should_Know,_Book_II (part), Songs_from_Books, The_Man_Who_Would_Be_King, The_Seven_Seas, The_Works_of_Rudyard_Kipling_One_Volume_Edition (Part), The_Years_Between, Verses_1889-1896
    "Samuel_Taylor_Coleridge": 0, # Poetry: Coleridge's_Ancient_Mariner_and_Select_Poems, Coleridge's_Literary_Remains,_Volume_1 (volume 1), The_Complete_Poetical_Works_of_Samuel_Taylor_Coleridge, The_Rime_of_the_Ancient_Mariner
    "Sinclair_Lewis": 0, # Prose
    "Sir_Arthur_Conan_Doyle": 0, # Poetry: Songs_of_Action, Songs_Of_The_Road, The_Guards_Came_Through_and_Other_Poems
    "Sir_Francis_Galton": 0, # Prose
    "Sir_Humphry_Davy": 0, # Prose
    "Sir_Isaac_Newton": 0, # Prose
    "Sir_Joseph_Dalton_Hooker": 0, # Prose
    "Sir_Richard_Francis_Burton": 0, # Poetry: The_Kasidah_of_Haji_Abdu_El-Yezdi
    "Sir_Walter_Scott": 0, # Poetry: Marmion, Minstrelsy_of_the_Scottish_border_(2_of_3) (parts), Some_Poems,  The_Lady_of_the_Lake
    "Sir_William_Schwenck_Gilbert": 1, # All Poetry
    "Stephen_Leacock": 0, # Prose
    "T_S_Eliot": 1, # Poetry: Poems, Prufrock_and_Other_Observations, The_Waste_Land
    "Thomas_Carlyle": 0, # Prose
    "Thomas_Crofton_Croker": 0, # Prose
    "Thomas_Hardy": 0, # Poetry: Late_Lyrics_and_Earlier, Moments_of_Vision, Poems_of_the_Past_and_the_Present, Satires_of_Circumstance, Time's_Laughingstocks_and_Other_Verses, Wessex_Poems_and_Other_Verses
    "Thomas_Henry_Huxley": 0, # Prose
    "Thomas_Robert_Malthus": 0, # Prose
    "Thornton_Waldo_Burgess": 0, # Prose
    "Ulysses_Grant": 0, # Prose
    "Virginia_Woolf": 0, # Prose
    "Walt_Whitman": 1, # Poetry: Drum_Taps, Leaves_of_Grass, Poems_By_Walt_Whitman, The_Patriotic_Poems_of_Walt_Whitman
    "Walter_de_la_Mare": 1, # Poetry:   Collected_Poems_1901-1918_in_Two_Volumes_Volume_1, Down-Adown-Derry, Peacock_Pie,_A_Book_of_Rhymes, Songs_of_Childhood, The_Listeners_and_Other_Poems
    "Washington_Irving": 0, # Prose
    "Wilkie_Collins": 0, # Prose
    "William_Blake": 1, # Poetry: Poems_of_William_Blake, Songs_of_Innocence_and_Songs_of_Experience; Short, no real text: Illustrations_of_The_Book_of_Job
    "William_Butler_Yeats": 0, # Poetry: In_The_Seven_Woods, Poems, Responsibilities, Seven_Poems_and_a_Fragment, The_Green_Helmet_and_Other_Poems, The_Land_Of_Heart's_Desire, The_Wild_Swans_at_Coole, The_Wind_Among_the_Reeds, Two_plays_for_dancers
    "William_Dean_Howells": 0, # Poetry: Poems
    "William_Ewart_Gladstone": 0, # Prose
    "William_Henry_Hudson": 0, # Prose
    "William_J_Long": 0, # Prose
    "William_Makepeace_Thackeray": 0, # Poetry: Ballads
    "William_Penn": 0, # Prose
    "William_Somerset_Maugham": 0, # Prose
    "William_Wordsworth": 1, # Poetry:   Lyrical_Ballads,_With_Other_Poems,_1800,_Volume_1, Poems_in_Two_Volumes,_Volume_1, The_Poetical_Works_of_William_Wordsworth,_Volume_1
    "William_Wymark_Jacobs": 0, # Prose
    "Winston_Churchill": 0, # Prose
    "Zane_Grey": 0, # Prose
    "Shakespeare": 1, # All Poetry
    "Anon_(Prik_of_Conscience)": 1, # Poetry
    "Chaucer": 0, # Mostly verse, some in prose
    "Gavin_Douglas": 1, # Poetry
    "George_Ashby": 1, # Poetry
    "John_Audelay": 1, # Poetry
    "John_Capgrave": 1, # Poetry
    "John_Gower": 1, # Poetry
    "John_Hardyng": 1, # Poetry
    "John_Lydgate": 1, # Poetry
    "John_Mandeville": 0, # Prose
    "John_Metham": 1, # Poetry
    "John_Mirk": 0, # Prose
    "Julian_of_Norwich": 0, # Prose
    "Laurence_Minot": 1, # Poetry
    "Margery_Kempe": 0, # Prose
    "Osbern_Bokenham": 1, # Poetry
    "Robert_Henryson": 1, # Poetry
    "Thomas_Hoccleve": 1, # Poetry
    "Thomas_Usk": 0, # Prose
    "Thomas_Mallory": 0, # Prose
    "Walter_Hilton": 0, # Prose
    "William_Caxton": 0, # Prose
    "William_Dunbar": 1, # Poetry
    "William_Paris": 1, # Poetry
    #
    "Anon_Árna": 0,
    "Anon_Bandamanna_K": 0,
    "Anon_Bandamanna_M": 0,
    "Anon_Ectors": 0,
    "Anon_Finnboga": 0,
    "Anon_Grágás": 0,
    "Anon_Grettis": 0,
    "Anon_Gunnars": 0,
    "Anon_Hómilíubók": 0,
    "Anon_Illuga": 0,
    "Anon_Jarlmanns": 0,
    "Anon_Jarteinabók": 0,
    "Anon_Jómsvíkinga": 0,
    "Anon_Júditarbók": 0,
    "Anon_Miðaldaævintýri": 0,
    "Anon_Morkinskinna": 0,
    "Anon_Mörtu": 0,
    "Anon_Sögu-þáttur": 0,
    "Anon_Vilhjálms": 0,
    "Anon_Víglundar": 0,
    "Anon_Þorláks": 0,
    "Arngrímur_Jónsson": 0,
    "Benedikt_Gröndal": 0,
    "Björn_Þorleifsson": 0,
    "Brandur_Jónsson": 0,
    "Einar_H_Kvaran": 0,
    "Einar_Kárason": 0,
    "Gestur_Pálsson": 0,
    "Gísli_Konráðsson": 0,
    "Guðmundur_Andri_Thorsson": 0,
    "Guðmundur_Einarsson": 0,
    "Halldór_Þorbergsson": 0,
    "Haraldur_Níelsson": 0,
    "Jón_Ólafsson_úr_Grunnavík": 0,
    "Jón_Halldórsson": 0,
    "Jón_Magnússon": 0,
    "Jón_Oddsson_Hjaltalín": 0,
    "Jón_Ólafsson_Indíafari": 0,
    "Jón_Steingrímsson": 0,
    "Jón_Thoroddsen": 0,
    "Jón_Trausti": 0,
    "Jón_Þorkelsson_Vídalín": 0,
    "Jón_Þorláksson": 0,
    "Jónas_Hallgrímsson": 0,
    "Oddur_Gottskálksson": 0,
    "Ólafur_Egilsson": 0,
    "Pétur_Gunnarsson": 0,
    "Pétur_Pétursson": 0,
    "Snorri_Sturluson": 0,
    "Sturla_Þórðarson": 0,
    "The_First_Grammarian": 0,
    "Torfhildur_Hólm": 0,
    "Þorgils_Gjallandi": 0,
    "Þorlákur_Skúlason": 0,
    "Þorsteinn_Björnsson": 0,
    "Þórarinn_Eldjárn": 0,
    "Anon_F1E": 0,
    "Anon_F01": 0,
    "Anon_F02": 0,
    "Anon_F03": 0,
    "Anon_F04": 0,
    "Anon_F05": 0,
    "Anon_F06": 0,
    "Anon_F07": 0,
    "Anon_F08": 0,
    "Anon_F09": 0,
    "Anon_F0A": 0,
    "Anon_F0B": 0,
    "Anon_F0C": 0,
    "Anon_F0E": 0,
    "Anon_F0D": 0,
    "Anon_F0F": 0,
    "Anon_F0K": 0,
    "Anon_F0G": 0,
    "Anon_F0H": 0,
    "Anon_F0I": 0,
    "Anon_F0J": 0,
    "Anon_F0L": 0,
    "Anon_F0M": 0,
    "Anon_F0N": 0,
    "Anon_F0O": 0,
    "Anon_F0P": 0,
    "Anon_F0Q": 0,
    "Anon_F0R": 0,
    "Anon_F1D": 0,
    "Anon_F0T": 0,
    "Anon_F0S": 0,
    "Anon_F0U": 0,
    "Anon_F0V": 0,
    "Anon_F0X": 0,
    "Anon_F11": 0,
    "Anon_F0Y": 0,
    "Anon_F12": 0,
    "Anon_F13": 0,
    "Anon_F14": 0,
    "Anon_F15": 0,
    "Anon_F16": 0,
    "Anon_F17": 0,
    "Anon_F18": 0,
    "Anon_F1A": 0,
    "Anon_F1B": 0,
    "Anon_F19": 0,
    "Anon_F1C": 0,
    "Anon_F1G": 0,
    "Anon_F1F": 0,
    "Ari_Kristján_Sæmundssen": 0,
    "Arnaldur_Birgir_Konráðsson": 0,
    "Arnaldur_Indriðason": 0,
    "Arnþór_Gunnarsson": 0,
    "Auður_Jónsdóttir": 0,
    "Álfheiður_Steinþórsdóttir": 0,
    "Ármann_Jakobsson": 0,
    "Árni_Bergmann": 0,
    "Árni_Björnsson": 0,
    "Bergþór_Pálsson": 0,
    "Birgitta_Jónsdóttir": 0,
    "Björn_Hróarsson": 0,
    "Bragi_Ólafsson": 0,
    "Einar_Kárason": 0,
    "Einar_Már_Guðmundsson": 0,
    "Elín_Vilhelmsdóttir": 0,
    "Elías_Snæland_Jónsson": 0,
    "Elísabet_Jökulsdóttir": 0,
    "Erla_Bolladóttir": 0,
    "Fríða_Á._Sigurðardóttir": 0,
    "Gerður_Kristný_Guðjónsdóttir": 0,
    "Gísli_Gunnarsson": 0,
    "Gísli_Sigurðsson": 0,
    "Guðjón_Ragnar_Jónasson": 0,
    "Guðmundur_Andri_Thorsson": 0,
    "Guðmundur_Eggertsson": 0,
    "Guðmundur_Pálmason": 0,
    "Guðrún_Eva_Mínervudóttir": 0,
    "Guðrún_Helgadóttir": 0,
    "Guðrún_Helgadóttir": 0,
    "Gunnar_Helgi_Kristinsson": 0,
    "Gunnar_Hersveinn": 0,
    "Gunnar_Karlsson": 0,
    "Hallgrímur_Helgason": 0,
    "Hanna_Björg_Sigurjónsdóttir": 0,
    "Harpa_Jónsdóttir": 0,
    "Harpa_Njálsdóttir": 0,
    "Helgi_Gunnlaugsson": 0,
    "Helgi_Skúli_Kjartansson": 0,
    "Hera_Karlsdóttir": 0,
    "Hermann_Óskarsson": 0,
    "Héðinn_Svarfdal_Björnsson": 0,
    "Hildur_Hákonardóttir": 0,
    "Hildurn_Helgadóttir": 0,
    "Hrund_Þórsdóttir": 0,
    "Hulda_Jensdóttir": 0,
    "Iðunn_Steinsdóttir": 0,
    "Ingi_Sigurðsson": 0,
    "Ingibjörg_Hjartardóttir": 0,
    "Ingibjörg_Haraldsdóttir": 0,
    "Íris_Ellenberger": 0,
    "Jóhanna_Einarsdóttir": 0,
    "Jón_Hallur_Stefánsson": 0,
    "Jón_Hnefill_Aðalsteinsson": 0,
    "Jón_Kalmann_Stefánsson": 0,
    "Jón_Karl_Helgason": 0,
    "Jón_Ólafur_Ísberg": 0,
    "Jón_R._Hjálmarsson": 0,
    "Jónas_Kristjánsson": 0,
    "Kristín_Björnsdóttir": 0,
    "Kristín_Steinsdóttir": 0,
    "Lára_Magnúsardóttir": 0,
    "Matthías_Johannessen": 0,
    "Oddný_Eir_Ævarsdóttir": 0,
    "Ólafur_Gunnarsson": 0,
    "Ólafur_Jóhann_Ólafsson": 0,
    "Páll_Rúnar_Elísson": 0,
    "Páll_Sigurðsson": 0,
    "Pétur_Gunnarsson": 0,
    "Pétur_Halldórsson": 0,
    "Ragnar_Arnalds": 0,
    "Ragnar_Gíslason": 0,
    "Reynir_Traustason": 0,
    "Róbert_Jack": 0,
    "Rósa_Eggertsdóttir": 0,
    "Sigmundur_Ernir_Rúnarsson": 0,
    "Sigríður_Dúna_Kristmundsdóttir": 0,
    "Sigríður_Gunnarsdóttir": 0,
    "Sigrún_Davíðsdóttir": 0,
    "Sigrún_Helgadóttir": 0,
    "Sigurður_A._Magnússon": 0,
    "Sigurjón_Magnússon": 0,
    "Sindri_Freysson": 0,
    "Símon_Jón_Jóhannsson": 0,
    "Skúli_Magnússon": 0,
    "Sólveig_Anna_Bóasdóttir": 0,
    "Stefanía_Valdís_Stefánsdóttir": 0,
    "Steingrímur_J._Sigfússon": 0,
    "Steinunn_Jóhannesdóttir": 0,
    "Steinar_Bragi": 0,
    "Steinunn_Sigurðardóttir": 0,
    "Súsanna_Svavarsdóttir": 0,
    "Thomas_Möller": 0,
    "Unnur_Jökulsdóttir": 0,
    "Úlfar_Hauksson": 0,
    "Úlfar_Þormóðsson": 0,
    "Vésteinn_Ólason": 0,
    "Viktor_Arnar_Ingólfsson": 0,
    "Þorbjörn_Broddason": 0,
    "Þorgrímur_Þráinsson": 0,
    "Þorvaldur_Gylfason": 0,
    "Þórarinn_Eldjárn": 0, # Already above from Icepahc, but accents seem to be an issue
    "Þórhallur_Heimisson": 0,
    "Þórunn_Hrefna_Sigurjónsdóttir": 0,
    "Þráinn_Bertelsson": 0,
    "Þröstur_Helgason": 0,
    "--------": 0,
    "Árni_Johnsen": 0,
    "Eyvindur_Karlsson": 0,
    "Vigdís_Grímsdóttir": 0,
    "Stefán_Máni": 0,
    "Þorleifur_Friðriksson": 0,
    "Sigurjón_Árni_Eyjólfsson": 0,
    "Rannveig_Traustadóttir": 0,
    "Huldar_Breiðfjörð": 0,
    "Bergsveinn_Birgisson": 0,
    "Nanna_Rögnvaldsdóttir": 0,
    "Pétur_H._Ármannson": 0,
    "Sigrún_Pálsdóttir": 0,
    "Baldur_Jónsson": 0,
}
def toGenre(name):
    if name[-2:] == "_2":
        name = name[:-2]

    if name[-6:] == "_Prose":
        return 0
    if name[-7:] == "_Poetry":
        return 1
    return namesToGenre[name]

# == PROSE:
# Romance: 0
# Speeches: 1
# Military/Historical Prose: 2
# Christian Prose: 3
# Other Prose: 4
# Philosophy: 5
# == POETRY:
# Comedy/Tragedy: 6
# Epic: 7
# Didactic: 8
# Other Poetry (Bucolic, Lyric, Hymn): 9
genreNarrowLabels = [
    "Romance",
    "Speeches",
    "Military/Historical Prose",
    "Christian Prose",
    "Other Prose",
    "Philosophy",
    "Comedy/Tragedy",
    "Epic",
    "Didactic",
    "Other Poetry"
]
namesToGenreNarrow = {
    "AchillesTatius": 0,
    "Aelian": 4,
    "AeneasTacticus": 1,
    "Aeschines": 1,
    "Aeschylus": 6,
    "Andocides": 1,
    "Antiphon": 1,
    "PseudoApollodorus": 4,
    "ApolloniusRhodius": 7,
    "Appian": 2,
    "AratusSolensis": 8,
    "Aretaeus": 4,
    "AeliusAristides": 1,
    "Aristophanes": 6,
    "Aristotle": 4,
    "Arrian": 2,
    "Asclepiodotus": 1,
    "Athenaeus": 4,
    "MarcusAurelius": 5,
    "Bacchylides": 9,
    "Barnabas": 3,
    "BasilBishopOfCaesarea": 3,
    "BionOfPhlossa": 9,
    "Callimachus": 9,
    "Callistratus": 4,
    "Chariton": 0,
    "ClementOfAlexandria": 3,
    "Colluthus": 7,
    "Demades": 1,
    "DemetriusOfPhaleron": 4,
    "Demosthenes": 1,
    "Dinarchus": 1,
    "DioChrysostom": 1,
    "CassiusDio": 2,
    "DiodorusSiculus": 2,
    "DiogenesLaertius": 4,
    "DionysiusOfHalicarnassus": 4,
    "Epictetus": 5,
    "Euclid": 4,
    "Euripides": 6,
    "EusebiusOfCaesarea": 2,
    "Galen": 4,
    "ValeriusHarpocration": 4,
    "Herodotus": 2,
    "Hesiod": 9,
    "Hippocrates": 4,
    "Homer": 7,
    "Anonymous(Hymns_Dionysus)": 9,
    "Anonymous(Hymns_Demeter)": 9,
    "Anonymous(Hymns_Apollo)": 9,
    "Anonymous(Hymns_Hermes)": 9,
    "Anonymous(Hymns_Aphrodite)": 9,
    "Anonymous(Hymns_Rest)": 9,
    "Hyperides": 1,
    "Isaeus": 1,
    "Isocrates": 1,
    "JohnOfDamascus": 3,
    "FlaviusJosephus": 1,
    "Longinus": 3,
    "Longus": 0,
    "Lucian": 4,
    "Lycophron": 6,
    "Lycurgus": 1,
    "Lysias": 1,
    "Moschus": 9,
    "Anon_Bios": 9,
    "Anon_Megara": 9,
    "Bible": 3,
    "Nonnus": 7,
    "Onasander": 1,
    "OppianOfApamea": 8,
    "Oppian": 8,
    "Parthenius": 0,
    "Pausanias": 4,
    "PhilostratusTheAthenian": 4,
    "PhilostratusMinor": 4,
    "PhilostratusTheLemnian": 4,
    "Pindar": 9,
    "Plato": 5,
    "Plutarch": 4,
    "Polybius": 2,
    "Procopius": 2,
    "PseudoPlutarch": 4,
    "PseudoXenophon": 4,
    "ClaudiusPtolemy": 4,
    "QuintusSmyrnaeus": 7,
    "Sophocles": 6,
    "Strabo": 4,
    "Theocritus": 9,
    "Theophrastus": 4,
    "Thucydides": 2,
    "Tryphiodorus": 7,
    "XenophonOfEphesus": 0,
    "Xenophon": 2
}
def toGenreNarrow(name):
    if name[-2:] == "_2":
        name = name[:-2]
    return namesToGenreNarrow[name]


genrePlaysBMLabels = [
    "Prose", # 0
    "Poetry", # 1
    "Plays", # 2
    "Bion/Moschus", # 3
    "Lycophron" # 4
]
namesToGenrePlaysBM = {
    "AchillesTatius": 0,
    "Aelian": 0,
    "AeneasTacticus": 0,
    "Aeschines": 0,
    "Aeschylus": 2,
    "Andocides": 0,
    "Antiphon": 0,
    "PseudoApollodorus": 0,
    "ApolloniusRhodius": 1,
    "Appian": 0,
    "AratusSolensis": 1,
    "Aretaeus": 0,
    "AeliusAristides": 0,
    "Aristophanes": 2,
    "Aristotle": 0,
    "Arrian": 0,
    "Asclepiodotus": 0,
    "Athenaeus": 0,
    "MarcusAurelius": 0,
    "Bacchylides": 1,
    "Barnabas": 0,
    "BasilBishopOfCaesarea": 0,
    "BionOfPhlossa": 3,
    "Callimachus": 1,
    "Callistratus": 0,
    "Chariton": 0,
    "ClementOfAlexandria": 0,
    "Colluthus": 1,
    "Demades": 0,
    "DemetriusOfPhaleron": 0,
    "Demosthenes": 0,
    "Dinarchus": 0,
    "DioChrysostom": 0,
    "CassiusDio": 0,
    "DiodorusSiculus": 0,
    "DiogenesLaertius": 0,
    "DionysiusOfHalicarnassus": 0,
    "Epictetus": 0,
    "Euclid": 0,
    "Euripides": 2,
    "EusebiusOfCaesarea": 0,
    "Galen": 0,
    "ValeriusHarpocration": 0,
    "Herodotus": 0,
    "Hesiod": 1,
    "Hippocrates": 0,
    "Homer": 1,
    "Anonymous(Hymns_Dionysus)": 1,
    "Anonymous(Hymns_Demeter)": 1,
    "Anonymous(Hymns_Apollo)": 1,
    "Anonymous(Hymns_Hermes)": 1,
    "Anonymous(Hymns_Aphrodite)": 1,
    "Anonymous(Hymns_Rest)": 1,
    "Hyperides": 0,
    "Isaeus": 0,
    "Isocrates": 0,
    "JohnOfDamascus": 0,
    "FlaviusJosephus": 0,
    "Longinus": 0,
    "Longus": 0,
    "Lucian": 0,
    "Lycophron": 4,
    "Lycurgus": 0,
    "Lysias": 0,
    "Moschus": 3,
    "Anon_Bios": 3,
    "Anon_Megara": 3,
    "Bible": 0,
    "Nonnus": 1,
    "Onasander": 0,
    "OppianOfApamea": 1,
    "Oppian": 1,
    "Parthenius": 0,
    "Pausanias": 0,
    "PhilostratusTheAthenian": 0,
    "PhilostratusMinor": 0,
    "PhilostratusTheLemnian": 0,
    "Pindar": 1,
    "Plato": 0,
    "Plutarch": 0,
    "Polybius": 0,
    "Procopius": 0,
    "PseudoPlutarch": 0,
    "PseudoXenophon": 0,
    "ClaudiusPtolemy": 0,
    "QuintusSmyrnaeus": 1,
    "Sophocles": 2,
    "Strabo": 0,
    "Theocritus": 1,
    "Theophrastus": 0,
    "Thucydides": 0,
    "Tryphiodorus": 1,
    "XenophonOfEphesus": 0,
    "Xenophon": 0
}
def toGenrePlaysBM(name):
    if name[-2:] == "_2":
        name = name[:-2]
    return namesToGenrePlaysBM[name]

# 323 BC - Hellenistic
# 31 BC - Actium

# 0: to 500 BC - Archaic
# 1: 500 BC to 323 BC  - Classical
# 2: 323 BC to 31 BC - Hellenistic
# 3: 31 BC to 200 AD - Early Empire
# 4: Post middle 200 AD - Later Empire

timeframeLabels = [
    "Archaic",
    "Classical",
    "Hellenistic",
    "Early Empire",
    "Late Empire"
]
namesToTimeframe = {
    "AchillesTatius": 3,
    "Aelian": 3,
    "AeneasTacticus": 1,
    "Aeschines": 1,
    "Aeschylus": 1,
    "Andocides": 1,
    "Antiphon": 1,
    "PseudoApollodorus": 3,
    "ApolloniusRhodius": 2,
    "Appian": 3,
    "AratusSolensis": 2,
    "Aretaeus": 3,
    "AeliusAristides": 3,
    "Aristophanes": 1,
    "Aristotle": 1,
    "Arrian": 3,
    "Asclepiodotus": 2,
    "Athenaeus": 4,
    "MarcusAurelius": 3,
    "Bacchylides": 1,
    "Barnabas": 3,
    "BasilBishopOfCaesarea": 4,
    "BionOfPhlossa": 2,
    "Callimachus": 2,
    "Callistratus": 4,
    "Chariton": 3,
    "ClementOfAlexandria": 3,
    "Colluthus": 4,
    "Demades": 1,
    "DemetriusOfPhaleron": 2,
    "Demosthenes": 1,
    "Dinarchus": 2,
    "DioChrysostom": 3,
    "CassiusDio": 3,
    "DiodorusSiculus": 3,
    "DiogenesLaertius": 4,
    "DionysiusOfHalicarnassus": 2,
    "Epictetus": 3,
    "Euclid": 2,
    "Euripides": 1,
    "EusebiusOfCaesarea": 4,
    "Galen": 3,
    "ValeriusHarpocration": 3,
    "Herodotus": 1,
    "Hesiod": 0,
    "Hippocrates": 1,
    "Homer": 0,
    "Anonymous(Hymns_Dionysus)": 0,
    "Anonymous(Hymns_Demeter)": 0,
    "Anonymous(Hymns_Apollo)": 0,
    "Anonymous(Hymns_Hermes)": 0,
    "Anonymous(Hymns_Aphrodite)": 0,
    "Anonymous(Hymns_Rest)": 0,
    "Hyperides": 1,
    "Isaeus": 1,
    "Isocrates": 1,
    "JohnOfDamascus": 4,
    "FlaviusJosephus": 3,
    "Longinus": 3,
    "Longus": 3,
    "Lucian": 3,
    "Lycophron": 2,
    "Lycurgus": 1,
    "Lysias": 1,
    "Moschus": 2,
    "Anon_Bios": 2,
    "Anon_Megara": 2,
    "Bible": 3,
    "Nonnus": 4,
    "Onasander": 3,
    "OppianOfApamea": 3,
    "Oppian": 3,
    "Parthenius": 2,
    "Pausanias": 3,
    "PhilostratusTheAthenian": 3,
    "PhilostratusMinor": 3,
    "PhilostratusTheLemnian": 3,
    "Pindar": 1,
    "Plato": 1,
    "Plutarch": 3,
    "Polybius": 2,
    "Procopius": 4,
    "PseudoPlutarch": 4,
    "PseudoXenophon": 4,
    "ClaudiusPtolemy": 3,
    "QuintusSmyrnaeus": 4,
    "Sophocles": 1,
    "Strabo": 3,
    "Theocritus": 2,
    "Theophrastus": 2,
    "Thucydides": 1,
    "Tryphiodorus": 4,
    "XenophonOfEphesus": 3,
    "Xenophon": 1
}
def toTimeframe(name):
    if name[-2:] == "_2":
        name = name[:-2]
    return namesToTimeframe[name]



# dialects
dialectLabels = [
    "Koine",  # 0
    "Attic",  # 1
    "Ionic",  # 2
    "Doric",  # 3
    "Homeric" # 4
]
namesToDialect = {
    "AchillesTatius": 1,
    "Aelian": 1, # attic, as best I can tell
    "AeneasTacticus": 1, # attic-ionic
    "Aeschines": 1,
    "Aeschylus": 1,
    "Andocides": 1,
    "Antiphon": 1,
    "PseudoApollodorus": 0, # looks attic/koine, δυναστείαν; ἀρχῆς
    "ApolloniusRhodius": 4,
    "Appian": 0, # looks like he's koine via Horace White
    "AratusSolensis": 4, # with attic features
    "Aretaeus": 2,
    "AeliusAristides": 0, # highly atticized koine
    "Aristophanes": 1,
    "Aristotle": 1,
    "Arrian": 1, # and a little bit of 2
    "Asclepiodotus": 0, # probably, but not totaly clear
    "Athenaeus": 0, #koine (or maybe attic)
    "MarcusAurelius": 0,
    "Bacchylides": 3,
    "Barnabas": 0, # probably koine; or at least attic
    "BasilBishopOfCaesarea": 0, # probably koine, or at least attic
    "BionOfPhlossa": 3, # epic w/ doricisms
    "Callimachus": 4,
    "Callistratus": 0, # probably koine; or at least attic
    "Chariton": 0, # probably koine; or at least attic
    "ClementOfAlexandria": 0, # probably koine; or at least attic
    "Colluthus": 4, # similar to nonnus
    "Demades": 1,
    "DemetriusOfPhaleron": 1,
    "Demosthenes": 1,
    "Dinarchus": 1,
    "DioChrysostom": 0, # probably koine; or at least attic
    "CassiusDio": 1, # immitating Thucydides
    "DiodorusSiculus": 0, # probably koine; or at least attic
    "DiogenesLaertius": 0, # probably koine; or at least attic
    "DionysiusOfHalicarnassus": 1,
    "Epictetus": 0,
    "Euclid": 0,
    "Euripides": 1,
    "EusebiusOfCaesarea": 0, # probably koine; or at least attic
    "Galen": 0, # probably koine; or at least attic
    "ValeriusHarpocration": 0, # probably koine; or at least attic
    "Herodotus": 2,
    "Hesiod": 4,
    "Hippocrates": 2,
    "Homer": 4,
    "Anonymous(Hymns_Dionysus)": 4,
    "Anonymous(Hymns_Demeter)": 4,
    "Anonymous(Hymns_Apollo)": 4,
    "Anonymous(Hymns_Hermes)": 4,
    "Anonymous(Hymns_Aphrodite)": 4,
    "Anonymous(Hymns_Rest)": 0,
    "Hyperides": 1,
    "Isaeus": 1,
    "Isocrates": 1,
    "JohnOfDamascus": 0, # probably koine; or at least attic
    "FlaviusJosephus": 0, # probably koine; or at least attic
    "Longinus": 0, # probably koine; or at least attic
    "Longus": 0, # probably koine; or at least attic
    "Lucian": 1,
    "Lycophron": 0, # probably koine; or at least attic
    "Lycurgus": 1,
    "Lysias": 1,
    "Moschus": 3,
    "Anon_Bios": 3,
    "Anon_Megara": 3,
    "Bible": 0,
    "Nonnus": 4,
    "Onasander": 0, # probably koine; or at least attic
    "OppianOfApamea": 4, # apparently
    "Oppian": 4, # apparently
    "Parthenius": 0,  # probably koine; or at least attic
    "Pausanias": 1, # Pausanias: Travel and Memory in Roman Greece pg 26
    "PhilostratusTheAthenian": 0,  # probably koine; or at least attic
    "PhilostratusMinor": 0,  # probably koine; or at least attic
    "PhilostratusTheLemnian": 0,  # probably koine; or at least attic
    "Pindar": 3,
    "Plato": 1,
    "Plutarch": 0,
    "Polybius": 0,
    "Procopius": 1,
    "PseudoPlutarch": 0, # probably koine; or at least attic
    "PseudoXenophon": 1,
    "ClaudiusPtolemy": 0,
    "QuintusSmyrnaeus": 4,
    "Sophocles": 1,
    "Strabo": 0, # probably koine; or at least attic
    "Theocritus": 3,
    "Theophrastus": 1,  # attic-koine, originally spoke lesbian
    "Thucydides": 1,
    "Tryphiodorus": 4,
    "XenophonOfEphesus": 0,
    "Xenophon": 1
}
def toDialect(name):
    if name[-2:] == "_2":
        name = name[:-2]
    return namesToDialect[name]

# create an object for displaying items colored by genre
def createLabelObj(authorNames, name, converter, labels):
    newY = []
    for n in authorNames:
        if (n[-2:] == "_2"):
            n = n[:-2]
        newY.append(converter[n])

    obj = {
        "name": name,
        "target": np.array(newY),
        "labels": labels
    }

    return obj


labelList = [
    lambda n: createLabelObj(n, "genre_", namesToGenre, genreLabels),
    lambda n: createLabelObj(n, "narrow_genre_", namesToGenreNarrow, genreNarrowLabels),
    lambda n: createLabelObj(n, "timeframe_", namesToTimeframe, timeframeLabels),
    lambda n: createLabelObj(n, "dialect_", namesToDialect, dialectLabels),
    lambda n: createLabelObj(n, "genre_plays_bm", namesToGenrePlaysBM, genrePlaysBMLabels),

]
