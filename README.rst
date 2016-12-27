PLN 2015: Procesamiento de Lenguaje Natural 2015 (Traitement Automatique du Langage Naturel)
================================================


Installation
-----------

1. Les modules et logiciels sont requis:

   - Git
   - Pip
   - Python 3.4 o posterior
   - TkInter
   - Virtualenv

   Python3 devrait déjà être présent sur les distributions Ubuntu depuis la version 14.04. La commande pour réaliser ces installations sur un système Debian ou Ubuntu est : ::

    sudo apt-get install git  python3-pip python3-tk virtualenv

2. Créer et activer un nouveau  `virtualenv <https://virtualenv.readthedocs.io/en/stable/>`_. Pour cela, il est plus facile d'utiliser   `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_.
   La commande pour l'installer est la suivante::

    sudo pip3 install virtualenvwrapper
    
   Ajouter la variable suivante dans le bash si il risque d'y avoir un conflit entre python2 et python3 ::
   
      export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

   Ajouter la ligne suivante à la fin du fichier ``.bashrc`` à l'aide de la commande::

    [[ -s "/usr/local/bin/virtualenvwrapper.sh" ]] && source "/usr/local/bin/virtualenvwrapper.sh"

   Créer un nouvel environnement intitulé `pln-2015`::

    mkvirtualenv --system-site-packages --python=/usr/bin/python3 pln-2015

3. Cloner le GitHub pour récupérer les données::

    git clone https://github.com/bobocharbo/PLN-2015.git

4. Installer les packages recquis mentionnés dans le fichier requirements.txt::

    cd pln-2015
    pip install -r requirements.txt


Exécution
---------

1. Activer l'environnemnt virtuel avec la commande::

    workon pln-2015

2. Exécutez le script de votre choix, par exemple::

    python languagemodeling/scripts/train.py -h


Testing
-------

Correr nose::

    nosetests

