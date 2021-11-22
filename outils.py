from PIL import Image
from os import path
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator, get_single_color_func
from matplotlib.patches import Patch #NEW
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, colors

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
        
def clean(terme):
  if terme.isalpha():
    return True
  elif '-' in terme and not terme.startswith('-'):
    terme = terme.replace("-", "")
    if terme.isalpha():
      return True
    else:
      return False
  else:
    return False 

def Palette (cat):
  """génère une palette de couleurs uniformément répartie dans la colormap ci dessous
  en fonction du nombre placé en paramètre. D'autres colormap peuvent être choisies.
  cf. https://matplotlib.org/stable/tutorials/colors/colormaps.html
  la répartition se fait en excluant la première et la dernière valeur """
  cmap = 'gist_rainbow'

  x = np.linspace(0.0, 1.0, len(cat)+2) # 2 en plus pour les exclure.
  rgb = cm.get_cmap(cmap)(x)[np.newaxis, :, :3]
  palette = dict()
  ind = 1 # on exclue la première et la dernière valeur
  for cle in cat: # une cle une couleur
    palette[cle] = rgb[0][ind] 
    ind += 1 
  return palette
  
def makeImage(text, palette, color_to_words, leg = True):
  default_color = 'grey'  # la couleur par défaut (si le mot pas présent dans
                          # le dico color_to_words)
  # Create a color function with single tone
  grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

  # Create a color function with multiple tones
  # grouped_color_func = GroupedColorFunc(color_to_words, default_color)

  wc = WordCloud(collocations=False, # vu qu'on additionne des textes...
                 background_color="white", max_words=600, 
                 normalize_plurals=False, # spacy l'a fait
                 width=1400, height=600).generate(text)
  plt.figure(figsize=(20, 15), facecolor=None)
  # pour avoir la légende
  if leg:
    legend = [Patch(facecolor=(colors.to_hex(palette [cle])), label=cle) for cle in palette.keys()] 
 
  wc.recolor(color_func=grouped_color_func)
  # plt.legend(handles=legend)

  plt.imshow(wc)
  # show
  #plt.imshow(wc, interpolation="bilinear")
  plt.axis("off")
  plt.show()
  
def makeImage2(text, palette, color_to_words, leg):
  # même fonction que ci-dessus mais qui prend un dico [mot] = occurrence (par ex. issu de Counter) et
  # non un texte
  default_color = 'grey'  # la couleur par défaut (si le mot pas présent dans
                          # le dico color_to_words)
  # Create a color function with single tone
  grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

  # Create a color function with multiple tones
  # grouped_color_func = GroupedColorFunc(color_to_words, default_color)

  wc = WordCloud(collocations=False, # vu qu'on additionne des textes...
                 background_color="white", max_words=200,
                 width=1400, height=600).generate_from_frequencies(text)
  plt.figure(figsize=(20, 15), facecolor=None)
  # pour avoir la légende
  legend = [Patch(facecolor=(colors.to_hex(palette[cle])), label=cle) for cle in palette.keys()] 
 
  wc.recolor(color_func=grouped_color_func)
  if leg:
    plt.legend(handles=legend)
  plt.axis("off")
  plt.imshow(wc)
  

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
