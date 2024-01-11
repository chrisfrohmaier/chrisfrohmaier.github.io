from pybtex.database.input import bibtex
import string


import calendar
months = dict((month, index) for index, month in enumerate(calendar.month_name) if month)


template_file = '''---
title: "${title}"
date: ${date}
pubtype: "Paper"
featured: true
description: "${abstract}"
tags: [${tags}]
image: ""
link: "${link}"
fact: ""
weight: 400
sitemap:
  priority : 0.2
---

${abstract}
'''


#open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file("FrohmaierContributingAuthor.bib")

#loop through the individual references
for bib_id in bibdata.entries:
    try:
      b = bibdata.entries[bib_id].fields
      title_in = b['title'].strip('{}')
      date_in = b['year']+'-'+f"{months[b['month']]:02d}"+'-01'
      link_in = b['adsurl']
      abstract_in = str(b['abstract']).replace('{','').replace('}','').replace('$','').replace('\\%','per cent').replace('\\','')
      print(b['keywords'])
      t = string.Template(template_file)
      result = t.safe_substitute(title=title_in, date=date_in, link=link_in, abstract=abstract_in, tags=str([x.strip() for x in b['keywords'].split(',')]).strip('[]'))
      print(result)
      f = open('./content/publications/paper_'+str(b['eprint'])+'.md', 'w')
      f.write(result)
      f.close()
    except:
       continue
    