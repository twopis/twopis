# Stores dictionaries that convert from words to parts of speech

# Based on classifications from Perseus' Morpheus
# 0: noun; 1: verb; 2: adj + numeral; 3: adv + exclam;
# 4: pron; 5: article; 6: prep; 7: conj; 8: partic
greek = {
  "καί": "7",
  "δέ": "8",
  "τῶν": "5",
  "τήν": "5",
  "τό": "5",
  "μέν": "8",
  "τοῦ": "5",
  "τῆς": "5",
  "τόν": "5",
  "ἐν": "6",
  "γάρ": "8",
  "τε": "8",
  "ὁ": "5",
  "τά": "5",
  "τούς": "5",
  "τοῖς": "5",
  "πρός": "6",
  "ἐπί": "6",
  "τῷ": "5",
  "οἱ": "5",
  "ὡς": "7", # conj/adv
  "ἀλλά": "3",
  "ἤ": "7",
  "κατά": "6",
  "εἰς": "6",
  "μή": "7",
  "ἄν": "8",
  "περί": "6",
  "οὐ": "3",
  "τῇ": "5",
  "ἡ": "5",
  "τάς": "5",
  "διά": "6",
  "οὐκ": "3",
  "ἐκ": "6",
  "ὅτι": "3", # adv / conj
  "ἐς": "6",
  "ὑπό": "6",
  "οὖν": "8",
  "εἶναι": "1",
  "εἰ": "7",
  "παρά": "6",
  "ταῦτα": "2",
  "δή": "8",
  "τοῦτο": "2",
  "ἀπό": "6",
  "οὐδέ": "8",
  "μετά": "6",
  "αὐτόν": "2",
  "τι": "4",
  "ἦν": "7", # conj (or exclam)
  "γε": "8",
  "αὐτῷ": "2",
  "αὐτοῦ": "2",
  "τις": "4",
  "αὐτῶν": "2",
  "οὔτε": "3",
  "ὦ": "3", # exclam
  "ταῖς": "5",
  "τούτων": "2",
  "αὐτοῖς": "2",
  "τί": "4",
  "ἔτι": "3",
  "νῦν": "3",
  "οὐδέν": "2",
  "ἐξ": "6",
  "ὧν": "4",
  "ὥστε": "3",
  "αὐτός": "2",
  "ὅ": "4",
  "ἐγώ": "4",
  "μοι": "4",
  "ὥσπερ": "3",
  "πάντα": "2", # adj (or adv)
  "αὐτούς": "2",
  "ἐστιν": "1",
  "οὕτως": "3",
  "ἄρα": "8",
  "μᾶλλον": "3",
  "ὑπέρ": "6",
  "αἱ": "5",
  "ἔφη": "1",
  "ἤδη": "3",
  "ἐπεί": "7",
  "οὕτω": "3",
  "μάλιστα": "3",
  "τότε": "3",
  "ἐστι": "1",
  "πόλιν": "0",
  "ἡμῖν": "4",
  "οὐχ": "3",
  "τ᾽": "8",
  "μόνον": "2",
  "πολλά": "2",
  "πρῶτον": "2",
  "δεῖ": "1",
  "τούτου": "2",
  "ἐστίν": "1",
  "ἅμα": "3",
  "μηδέ": "8",
  "αὐτήν": "2",
  "μήτε": "8",
  "ἅ": "5",
  "ἵνα": "7", # conj (or adv)
  "με": "4",
  "τούτοις": "2",
  "σύ": "4",
  "οἵ": "4",
  "ἄλλων": "2",
  "ὅς": "4",
  "πάντων": "2",
  "μήν": "8",
  "πάλιν": "3",
  "ἐστί": "1",
  "σοι": "4", # pron (or adj)
  "ἔστι": "1",
  "ὑμῖν": "4",
  "οὗτος": "2",
  "ἔχει": "1",
  "ἐάν": "7",
  "εἴ": "7",
  "πῶς": "4", # pron or adv
  "δύο": "2", # numeral
  "τοῦτον": "2",
  "οἷς": "4",
  "ἔχειν": "1",
  "ὅπως": "7",
  "πρότερον": "2",
  "αὐτό": "2",
  "ὅταν": "7",
  "τινα": "4",
  "πολύ": "2",
  "ἡμᾶς": "4",
  "γενέσθαι": "1",
  "ἡμῶν": "4",
  "αὐτῆς": "2",
  "ἀεί": "3",
  "ἥν": "4",
  "λόγον": "0",
  "πόλεως": "0",
  "λέγειν": "1",
  "τούτῳ": "2",
  "ταύτην": "2",
  "ὅν": "4",
  "μηδέν": "2",
  "Σωκράτης": "0",
  "ὥς": "7", # conj or adv
  "εἰπεῖν": "1",
  "ὑμᾶς": "4",
  "οὗ": "3",
  "Χορός": "0",
  "τοι": "8", # partic or pronoun
  "μιν": "4",
  "σε": "4",
  "ἦ": "3",
  "ἀμφί": "6",
  "αὐτάρ": "8",
  "Διός": "2",
  "τίς": "4",
  "σ᾽": "4",
  "ἐνί": "0",
  "σύν": "6",
  "περ": "8",
  "μέγα": "2",
  "θεῶν": "0",
  "ὅτε": "7",
  "ἐμοί": "4",
  "οὔ": "3",
  "ἔνθα": "3",
  "ἥ": "5",
  "ἔχων": "1", # part
  "εὖ": "3",
  "ἀνήρ": "0",
  "κεν": "8",
  "Ζεύς": "0",
  "πατρός": "0",
  "οἷον": "2",
  "μέντοι": "8",
  "ὤν": "1", # participle
  "σε": "4",
  "εἴη": "1",
  "σύν": "6",
  "ἔστιν": "1",
  "χρόνον": "0",
  "εὖ": "3",
  "πάντες": "2",
  "ἀνθρώπων": "0",
  "ᾧ": "4",
  "αὐτοί": "2",
  "ἄλλα": "2",
  "μέχρι": "6", # LSJ: "used chiefly in Prose and before a Prep"
  "ὅσα": "2",
  "τοίνυν": "8",
  "ὑμῶν": "4",
  "ἄνδρες": "0",
  "εὐθύς": "2",
}
# 0: noun; 1: verb; 2: adj + numeral; 3: adv + exclam;
# 4: pron; 5: article; 6: prep; 7: conj; 8: partic

# Grouping words by their final letter.
#ν: 0, ς: 1, κ: 2, ρ: 3, ε: 4; ο: 5; α: 6; ι: 7; υ: 8; ω: 9; η : 10
# greek = {
#   "καί": "7",
#   "δέ": "4",
#   "τῶν": "0",
#   "τήν": "0",
#   "τό": "5",
#   "μέν": "0",
#   "τοῦ": "8",
#   "τῆς": "1",
#   "τόν": "0",
#   "ἐν": "0",
#   "γάρ": "3",
#   "τε": "4",
#   "ὁ": "5",
#   "τά": "6",
#   "τούς": "1",
#   "τοῖς": "1",
#   "πρός": "1",
#   "ἐπί": "7",
#   "τῷ": "9",
#   "οἱ": "7",
#   "ὡς": "1",
#   "ἀλλά": "6",
#   "ἤ": "10",
#   "κατά": "6",
#   "εἰς": "1",
#   "μή": "10",
#   "ἄν": "0",
#   "περί": "7",
#   "οὐ": "8",
#   "τῇ": "10",
#   "ἡ": "10",
#   "τάς": "1",
#   "διά": "6",
#   "οὐκ": "2",
#   "ἐκ": "2",
#   "ὅτι": "7",
#   "ἐς": "1",
#   "ὑπό": "5",
#   "οὖν": "0",
#   "εἶναι": "7",
#   "εἰ": "7",
#   "παρά": "6",
#   "ταῦτα": "6",
#   "δή": "10",
#   "τοῦτο": "5",
#   "ἀπό": "5",
#   "οὐδέ": "4",
#   "μετά": "6",
#   "αὐτόν": "0",
#   "τι": "7",
#   "ἦν": "0",
#   "γε": "4",
#   "αὐτῷ": "9",
#   "αὐτοῦ": "8",
#   "τις": "1",
#   "αὐτῶν": "0",
#   "οὔτε": "4",
#   "ὦ": "9",
#   "ταῖς": "1",
#   "τούτων": "0",
#   "αὐτοῖς": "1",
#   "τί": "7",
#   "ἔτι": "7",
#   "νῦν": "0",
#   "οὐδέν": "0",
#   "ἐξ": "1",
#   "ὧν": "0",
#   "ὥστε": "4",
#   "αὐτός": "1",
#   "ὅ": "5",
#   "ἐγώ": "9",
#   "μοι": "7",
#   "ὥσπερ": "3",
#   "πάντα": "6",
#   "αὐτούς": "1",
#   "ἐστιν": "0",
#   "οὕτως": "1",
#   "ἄρα": "6",
#   "μᾶλλον": "0",
#   "ὑπέρ": "3",
#   "αἱ": "7",
#   "ἔφη": "10",
#   "ἤδη": "10",
#   "ἐπεί": "7",
#   "οὕτω": "9",
#   "μάλιστα": "6",
#   "τότε": "4",
#   "ἐστι": "7",
#   "πόλιν": "0",
#   "ἡμῖν": "0",
#   "οὐχ": "2",
#   "τ᾽": "11",
#   "μόνον": "0",
#   "πολλά": "6",
#   "πρῶτον": "0",
#   "δεῖ": "7",
#   "τούτου": "8",
#   "ἐστίν": "0",
#   "ἅμα": "6",
#   "μηδέ": "4",
#   "αὐτήν": "0",
#   "μήτε": "4",
#   "ἅ": "6",
#   "ἵνα": "6",
#   "με": "4",
#   "τούτοις": "1",
#   "σύ": "8",
#   "οἵ": "7",
#   "ἄλλων": "0",
#   "ὅς": "1",
#   "πάντων": "0",
#   "μήν": "0",
#   "πάλιν": "0",
#   "ἐστί": "7",
#   "σοι": "7",
#   "ἔστι": "7",
#   "ὑμῖν": "0",
#   "οὗτος": "1",
#   "ἔχει": "7",
#   "ἐάν": "0",
#   "εἴ": "7",
#   "πῶς": "1",
#   "δύο": "5",
#   "τοῦτον": "0",
#   "οἷς": "1",
#   "ἔχειν": "0",
#   "ὅπως": "1",
#   "πρότερον": "0",
#   "αὐτό": "5",
#   "ὅταν": "0",
#   "τινα": "6",
#   "πολύ": "8",
#   "ἡμᾶς": "1",
#   "γενέσθαι": "7",
#   "ἡμῶν": "0",
#   "αὐτῆς": "1",
#   "ἀεί": "7",
#   "ἥν": "0",
#   "λόγον": "0",
#   "πόλεως": "1",
#   "λέγειν": "0",
#   "τούτῳ": "9",
#   "ταύτην": "0",
#   "ὅν": "0",
#   "μηδέν": "0",
#   "Σωκράτης": "1",
#   "ὥς": "1",
#   "εἰπεῖν": "0",
#   "ὑμᾶς": "1",
#   "οὗ": "8",
#   "Χορός": "1",
#   "τοι": "7",
#   "μιν": "0",
#   "σε": "4",
#   "ἦ": "10",
#   "ἀμφί": "7",
#   "αὐτάρ": "3",
#   "Διός": "1",
#   "τίς": "1",
#   "σ᾽": "1",
#   "ἐνί": "7",
#   "σύν": "0",
#   "περ": "3",
#   "μέγα": "6",
#   "θεῶν": "0",
#   "ὅτε": "4",
#   "ἐμοί": "7",
#   "οὔ": "8",
#   "ἔνθα": "6",
#   "ἥ": "10",
#   "ἔχων": "0",
#   "εὖ": "8",
#   "ἀνήρ": "3",
#   "κεν": "0",
#   "Ζεύς": "1",
#   "πατρός": "1",
# }

english = {}

icelandic = {}
