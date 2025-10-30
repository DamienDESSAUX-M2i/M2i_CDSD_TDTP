# Les commandes pour donner les droits au dossier essai_droit sont,
# en notation symbolique :
chmod o-r essai_droit
chmod u-w essai_droit | chmod g-rx essai_droit | chmod g+w essai_droit | chmod o-r essai_droit
chmod u-rx essai_droit | chmod g-r essai_droit | chmod o-x essai_droit
chmod u-rw essai_droit | chmod o-rx essai_droit

# en base 8:
chmod 751 essai_droit
chmod 521 essai_droit
chmod 214 essai_droit
chmod 150 essai_droit