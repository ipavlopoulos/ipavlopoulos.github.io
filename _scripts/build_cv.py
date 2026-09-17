#!/usr/bin/env python3
"""Assemble cv-full.md from the pages that already hold each list.

The CV repeats what publications.md, talks.md, theses.md and projects.md
say, so it is generated from them rather than kept in step by hand.
Run from the repository root after editing any of those pages:

    python3 _scripts/build_cv.py
"""

import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAST_UPDATED = "September 2026"


def body(name):
    """Page content with the YAML front matter stripped."""
    text = io.open(os.path.join(ROOT, name), encoding="utf-8").read()
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S).strip()


# The source pages use lower-case headings; a CV reads better with proper ones,
# and "theses" there means Pavlopoulos' own, not the supervised ones listed above.
HEADINGS = {
    "accepted papers": "Accepted papers",
    "publications in proceedings of peer-reviewed venues":
        "Publications in proceedings of peer-reviewed venues",
    "book chapters": "Book chapters",
    "journals": "Journal articles",
    "preprints": "Preprints",
    "theses": "Doctoral and master's theses",
}


def demote(text):
    """Push the source page's headings one level down, under the CV's own."""
    def rewrite(match):
        return "### " + HEADINGS.get(match.group(1), match.group(1))
    return re.sub(r"^## (.+)$", rewrite, text, flags=re.M)


def between(text, start, end=None):
    text = text.split(start, 1)[1]
    return (text.split(end, 1)[0] if end else text).strip()


publications = demote(body("publications.md").replace(
    "(find me on [Google Scholar](https://scholar.google.com/citations?user=niKjjdEAAAAJ&hl=en))",
    "").strip())
talks = demote(between(body("talks.md"), "## Recent talks", "## Recorded talks"))
# theses.md ends with a note on supervision requests; the CV stops before it.
theses = body("theses.md").split("\n---\n")[0].strip()
projects = body("projects.md")

STATIC = u"""---
layout: default
permalink: /cv/full/
---

# John Pavlopoulos

**Curriculum Vitae** — last updated {updated}. Also available as PDF, in
[English]({{{{ '/files/cv_en.pdf' | relative_url }}}}) and
[Greek]({{{{ '/files/cv_gr.pdf' | relative_url }}}}), or as a
[short version]({{{{ '/files/cv_short_en.pdf' | relative_url }}}}).

Assistant Professor of Machine Learning, Department of Informatics, Athens
University of Economics and Business. Researcher at Archimedes, Athena Research
Center, and affiliated with Stockholm University.

* E-mail: ipavlopoulos (or annis) at aueb dot gr
* Office: Antoniadou Wing, 3rd Floor (A308), Patision 76, Athens 104 34
* Phone: +30 210 82 03 133
* Web: [ipavlopoulos.github.io](https://ipavlopoulos.github.io); [Google Scholar](https://scholar.google.com/citations?user=niKjjdEAAAAJ&hl=en)

## Research interests

Machine learning for Natural Language Processing, with applications in the
Social Sciences and Humanities, and in Healthcare. In particular: machine and
deep learning for text and images; mining emotion and named entities from large
collections; classification for early diagnosis or filtering; and natural
language generation.

## Education

* **2010–2014** — PhD in Natural Language Processing, "Aspect Based Sentiment
  Analysis". Department of Informatics, Athens University of Economics and
  Business, Greece. Supervisor: Professor Ion Androutsopoulos.
* **2008–2009** — MSc in Artificial Intelligence, School of Informatics,
  University of Edinburgh, UK. Dissertation supervised by Professor Mirella Lapata.
* **2001–2007** — School of Applied Mathematics and Physical Sciences, National
  Technical University of Athens, Greece.

## Academic and professional experience

* **Athens University of Economics and Business**, Department of Informatics —
  Assistant Professor of Machine Learning.
* **Archimedes, Athena Research Center** — Researcher.
* **Stockholm University**, Department of Computer and Systems Sciences —
  Senior Lecturer (fixed-term) in NLP and Data Science (2020–2021);
  Postdoctoral Researcher (2019–2020); currently affiliated.
* **Ca' Foscari University of Venice**, Department of Humanities — Visiting
  Scholar in NLP at the Venice Centre for Digital and Public Humanities
  (2021–2022). Co-organised the HTREC academic challenge.
* **Google Jigsaw** — Research associate (from 2018).
* **Cognitiv+** — Data Scientist (2018–2019). Layout and skew detection in
  images of legal documents; data annotation manager.
* **Liquid Media / Straintek** — Senior Researcher (2016–2018), leading the team
  developing APIs for multilingual abusive language detection; Postdoctoral
  Researcher (2015–2016).
* **Hellenic Army** — Software development (2014–2015).
* **BioASQ** — Research associate (2012–2014).

## Teaching

Currently teaching Natural Language Processing (MSc in Digital Methods for the
Humanities), Programming with Java (BSc), and Data Mining (BSc) at the Athens
University of Economics and Business.

Previously: Practical Data Science (MS in Data Science, AUEB); Natural Language
Processing (PhD course, Stockholm University); Visiting Lecturer in Data Science
(Stockholm University).

## Scholarships and awards

* Google Research Award for postdoctoral studies.
* Best paper, 27th International Conference on Discovery Science (2024).
* Best paper, 1st Workshop on Machine Learning for Ancient Languages (2024).
* PriceWaterhouseCoopers scholarship for postgraduate studies.
* Thomaidio Award for the best BSc thesis in the university.
* Ganioti-Papageorgi scholarship for undergraduate studies.
* Aglaias Koufodimou scholarship for undergraduate studies.

## Service

Member of the editorial board of *magazén*, International Journal for Digital
and Public Humanities. Member of the organising committee of the ML4AL ACL
workshop and of the programme committee of the Abusive Language Workshop.
Reviewer for NeurIPS, ACL, EMNLP, COLING and NAACL-HLT, and for journals
including Natural Language Engineering and Data Mining and Knowledge Discovery.

## Research projects

{projects}

## Invited talks and session coordination

{talks}

## Thesis supervision

{theses}

## Publications

{publications}
"""

out = STATIC.format(updated=LAST_UPDATED, projects=projects, talks=talks,
                    theses=theses, publications=publications)
io.open(os.path.join(ROOT, "cv-full.md"), "w", encoding="utf-8").write(out)
print("wrote cv-full.md (%d lines)" % out.count("\n"))
