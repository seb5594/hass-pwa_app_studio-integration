# Installer, coupler et mettre à jour une application web

## Envoyer un tableau de bord à quelqu'un que vous connaissez

Exemple. Sebastian crée une application Web qui affiche les départs des trains. Son oncle utilise déjà l'application officielle Home Assistant Companion et a accès au tableau de bord. Sebastian envoie le lien du navigateur via WhatsApp.

1. Dans PWA Web-App Studio, ouvrez l'application, accédez à Access, activez la connexion via l'application Companion et enregistrez. Les deux applications doivent atteindre le même serveur Home Assistant via HTTPS.

2. Votre invité ouvre le lien WhatsApp dans son navigateur et choisit Se connecter via l'application Companion. L'application Web affiche un code d'appareil. Le voyageur peut le copier si nécessaire.

3. Appuyez sur Ouvrir Home Assistant. Confirmez que l'application, le compte et le code correspondent. Si la page de couplage demande un code, collez ou saisissez le code affiché dans l'application Web. Approuvez ensuite la connexion.

4. Revenez à l'onglet d'origine du navigateur. Il se connecte automatiquement. Si nécessaire, appuyez sur Vérifier l'approbation. Le code est valable cinq minutes et pour une seule connexion.

5. Sur iPhone ou iPad, pour vous connecter à la copie installée, ajoutez d'abord la page à l'écran d'accueil de Safari. Ouvrez l’icône de l’écran d’accueil et démarrez-y le même processus d’approbation.

## Trouver le studio

Utilisez le matériel d'intégration, puis ouvrez le Studio via la boîte de dialogue Home Assistant. Si vous travaillez fréquemment sur des applications, activez l'entité de commutateur du panneau de la barre latérale dans les paramètres d'intégration et activez-la pour garder le raccourci visible.

Pour un tableau de bord de maintenance, ajoutez une carte de bouton qui permet d'accéder à /pwa-app-studio. L’entité facultative du bouton Ouvrir PWA Designer peut également l’ouvrir dans votre session d’administrateur active. Activez d’abord cette entité ; Home Assistant le désactive par défaut.

## Concevoir et mettre à jour un tableau de bord invité

Par exemple, créez un tableau de bord pour les visiteurs avec une carte d'information Wi-Fi et une lumière de terrasse. Sous Contenu, choisissez des cartes individuelles et sélectionnez un préréglage ou importez une carte existante. Définissez le titre, l'entité ou Markdown à l'aide de l'éditeur visuel et vérifiez l'aperçu du téléphone.

À l'étape Application, définissez la version de l'application sur 1.1 et enregistrez. Un invité dont l'application est toujours ouverte voit une bannière de mise à jour lorsque l'application détecte la nouvelle révision. Appuyer sur Mettre à jour l'application recharge la vue et conserve l'icône de l'écran d'accueil et la session du navigateur. Une application ouverte plus tard charge la version actuelle une fois connectée.

## Partager depuis Android

Utiliser le partage de lien dans le Studio. La boîte de dialogue native s'ouvre lorsque l'application ou le navigateur la fournit. Si l'application Companion ne propose aucune API de partage, ouvrez la page de partage dans le navigateur. Vous pouvez également copier le lien.

[English README](../README.md) · [Deutsch](../README.de.md)
