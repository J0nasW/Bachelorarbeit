(TeX-add-style-hook
 "lrt_thesis"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("graphicx" "pdftex")))
   (TeX-run-style-hooks
    "graphicx"
    "natbib"
    "color"
    "framed"
    "enumitem"
    "abbrevs")
   (TeX-add-symbols
    "endfigure"
    '("leftfigure" ["argument"] 1)
    '("foreword" ["argument"] 0)
    '("preface" ["argument"] 0)
    '("motto" ["argument"] 1)
    '("keywords" 1)
    '("probref" 1)
    '("allmodesymb" 2)
    '("greeksymbold" 1)
    '("greeksym" 1)
    '("Extrachap" 1)
    '("extrachap" 1)
    '("chapauthor" 1)
    '("chapsubtitle" 1)
    "etal"
    "svparindent"
    "betweenumberspace"
    "headlineindent"
    "LArge"
    "partnumsize"
    "partnumstyle"
    "partsize"
    "partstyle"
    "chapnumsize"
    "chapnumstyle"
    "chapsize"
    "chapstyle"
    "chapauthsize"
    "chapauthstyle"
    "mottosize"
    "mottostyle"
    "secsize"
    "secstyle"
    "subsecsize"
    "subsecstyle"
    "subsubsecstyle"
    "clearemptydoublepage"
    "startnewpage"
    "fronttitlepage"
    "frontmatter"
    "mainmatter"
    "backmatter"
    "mottowidth"
    "processmotto"
    "processchapsubtit"
    "processchapauthor"
    "chapter"
    "runinhead"
    "subruninhead"
    "svitemindent"
    "verbatimindent"
    "D"
    "E"
    "I"
    "Gamma"
    "Delta"
    "Theta"
    "Lambda"
    "Xi"
    "Pi"
    "Sigma"
    "Upsilon"
    "Phi"
    "Psi"
    "Omega"
    "varGamma"
    "varDelta"
    "varTheta"
    "varLambda"
    "varXi"
    "varPi"
    "varSigma"
    "varUpsilon"
    "varPhi"
    "varPsi"
    "varOmega"
    "ualpha"
    "ubeta"
    "uchi"
    "udelta"
    "ugamma"
    "umu"
    "unu"
    "upi"
    "utau"
    "qedsymbol"
    "qed"
    "smartqed"
    "tocchpnum"
    "tocsecnum"
    "tocsectotal"
    "tocsubsecnum"
    "tocsubsectotal"
    "tocsubsubsecnum"
    "tocsubsubsectotal"
    "tocparanum"
    "tocparatotal"
    "tocsubparanum"
    "nocaption"
    "spthmsep"
    "instindent"
    "figgap"
    "figcapgap"
    "tabcapgap"
    "abstract"
    "bibfont"
    "envankh"
    "svlanginfo"
    "url"
    "nixchapnum"
    "numstyle"
    "makereferee"
    "oribibl"
    "secbibl"
    "ClassInfoNoLine"
    "FrameCommand"
    "baselinestretch"
    "footnotesize"
    "textfraction"
    "floatpagefraction"
    "topfraction"
    "bottomfraction"
    "cleardoublepage"
    "seccounterend"
    "seccountergap"
    "firstmark"
    "thechapterend"
    "everypar"
    "runinsep"
    "aftertext"
    "thesection"
    "thesubsection"
    "thesubsubsection"
    "mpicplace"
    "setitemindent"
    "setitemitemindent"
    "description"
    "describelabel"
    "itemize"
    "enumerate"
    "makelabel"
    "verbatim"
    "eul"
    "imag"
    "vec"
    "tens"
    "thesubequation"
    "thisbottomragged"
    "propositionname"
    "definitionname"
    "lemmaname"
    "problemname"
    "abstractname"
    "ackname"
    "andname"
    "lastandname"
    "appendixname"
    "chaptername"
    "claimname"
    "conjecturename"
    "contentsname"
    "corollaryname"
    "emailname"
    "examplename"
    "exercisename"
    "figurename"
    "forewordname"
    "keywordname"
    "indexname"
    "contriblistname"
    "listfigurename"
    "listtablename"
    "mailname"
    "noteaddname"
    "notename"
    "partname"
    "prefacename"
    "proofname"
    "propertyname"
    "questionname"
    "refname"
    "remarkname"
    "seename"
    "solutionname"
    "solutionNOname"
    "subclassname"
    "tablename"
    "theoremname"
    "getsto"
    "lid"
    "gid"
    "grole"
    "bbbr"
    "bbbm"
    "bbbn"
    "bbbf"
    "bbbh"
    "bbbk"
    "bbbp"
    "bbbone"
    "bbbc"
    "bbbq"
    "bbbt"
    "bbbs"
    "bbbz"
    "svhline"
    "tableofcontents"
    "addnumcontentsmark"
    "addcontentsmark"
    "addcontentsmarkwop"
    "addtocmark"
    "calctocindent"
    "iand"
    "nand"
    "at"
    "spnewtheorem"
    "normalthmheadings"
    "reversethmheadings"
    "spdefaulttheorem"
    "floatlegendstyle"
    "floatcounterend"
    "capstrut"
    "twocaptionwidth"
    "leftcaption"
    "rightcaption"
    "rightfigure"
    "sidecaption"
    "captionstyle"
    "leftlegendglue"
    "subfigures"
    "thefigure"
    "resetsubfig"
    "samenumber"
    "biblstarthook"
    "bibsection"
    "protect"
    "bibname"
    "threecolindex"
    "indexstarthook"
    "item"
    "idxquad"
    "subitem"
    "subsubitem"
    "indexspace"
    "subtitle"
    "thesistype"
    "maketitle"
    "advisor"
    "examiner"
    "abgabedatum"
    "fronttitle"
    "thefootnote"
    "finalmatter"
    "thanks"
    "and"
    "runheadsize"
    "runheadstyle"
    "customizhead"
    "chaptermark"
    "sectionmark"
    "subsectionmark"
    "skipextosol")
   (LaTeX-add-environments
    '("eqnbox" LaTeX-env-args ["argument"] 0)
    "tinted"
    "defined"
    "definitionbox"
    "theoremed"
    "theorembox"
    "eqned"
    "lemmaed"
    "lemmabox"
    "exercised"
    "exercisebox"
    "solved"
    "solutionbox"
    "remarked"
    "remarkbox"
    "petit"
    "partbacktext"
    "dedication"
    "svgraybox"
    "svtintedbox"
    "thecontriblist"
    "theopargself"
    "sol"
    "acknowledgement"
    "noteadd"
    "subexample"
    "listenum")
   (LaTeX-add-pagestyles
    "bchap"
    "headings"
    "myheadings")
   (LaTeX-add-counters
    "chapter"
    "merk")
   (LaTeX-add-lengths
    "eqnvskip")
   (LaTeX-add-color-definecolors
    "shadecolor"
    "whitecolor"
    "tintedcolor"
    "definitioncolor"
    "exercisecolor"
    "solutioncolor"
    "lightcoralcolor"
    "theoremcolor"
    "lemmacolor"
    "eqncolor"
    "remarkcolor")))

