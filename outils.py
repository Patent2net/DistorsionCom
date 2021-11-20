def get_lang_detector(nlp, name):
    return LanguageDetector()
    

def isPartner(url, listPart):
  # pour comparer les urls on les découpe sur la partie du nom serveur
  url = url.strip()
  url = url.replace('"', "")
  urlP = parse.urlparse(url)
  urlP = urlP.scheme + '://' + urlP.hostname
  return urlP in listPart
  
# pompé là : https://amueller.github.io/word_cloud/auto_examples/colored_by_group.html
# voir la doc exemple en fin de code sur le lien. Supprimé ici pour écouter.
# deux types de coloration : binaire pour une couleur à un "type de mots" ou un dégradé 
# pour un type de mots. Peut-être que le dégradé peut se contrôler sur la fréquence 
# du mot mais j'ai pas essayé. Je préfère le SimpleGrouped... plus facilement interprétable
# tant que le dégradé ne porte pas un indicateur particulier.

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)
        
