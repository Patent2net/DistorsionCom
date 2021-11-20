def isPartner(url, listPart):
  # pour comparer les urls on les découpe sur la partie du nom serveur
  url = url.strip()
  url = url.replace('"', "")
  urlP = parse.urlparse(url)
  urlP = urlP.scheme + '://' + urlP.hostname
  return urlP in listPart
  
