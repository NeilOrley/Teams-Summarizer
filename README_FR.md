# Teams-Summarizer

- [English version](README.md)

![License](https://img.shields.io/badge/License-MIT-blue.svg)

**Teams-Summarizer** est une application qui permet de générer automatiquement des résumés à partir de fichiers VTT, généralement utilisés pour stocker des sous-titres ou des transcriptions. Conçu pour aider à résumer rapidement les longues conversations ou réunions, cet outil offre à la fois une interface utilisateur web simple et une interface en ligne de commande.

## Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Web UI](#web-ui)
  - [Command Line Interface (CLI)](#command-line-interface-cli)
- [Configuration](#configuration)
- [License](#license)
- [Support](#support)
- [Contribution](#contribution)

## Installation

1. **Clonez ce dépôt** :
   
   ```bash
   git clone https://github.com/NeilOrley/Teams-Summarizer.git
   cd Teams-Summarizer
   ```

2. **Installez les dépendances** :
   
   Assurez-vous d'avoir Python installé et utilisez la commande suivante pour installer toutes les dépendances nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Web UI

Pour démarrer l'interface utilisateur web :

```bash
python app.py
```

Cela lancera un serveur web local. Vous pouvez accéder à l'application via votre navigateur à l'adresse `http://localhost:5000`.

### Command Line Interface (CLI)

Pour utiliser l'application en ligne de commande :

```bash
python cli_summarize.py --file_path=path_to_vtt_file.vtt
```

### Configuration

Pour que l'application fonctionne, vous devez disposer d'une clé API OpenAI. Une fois que vous avez votre clé, veuillez la configurer dans le fichier `config.ini`.

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Support

Aucun support n'est assuré pour cette application. Cependant, vous pouvez toujours ouvrir des [issues](https://github.com/NeilOrley/Teams-Summarizer/issues) sur GitHub si vous rencontrez des problèmes ou si vous avez des suggestions.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des pull requests ou à soumettre des issues sur [GitHub](https://github.com/NeilOrley/Teams-Summarizer).

> ---
>
> _Note : Ce texte a été généré avec l'aide de ChatGPT, un modèle linguistique développé par OpenAI._