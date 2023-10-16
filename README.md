# Teams-Summarizer

- [French version](README_FR.md)

![License](https://img.shields.io/badge/License-MIT-blue.svg)

**Teams-Summarizer** is an application that allows for automatic generation of summaries from VTT files, commonly used to store subtitles or transcriptions. Designed to help quickly summarize long conversations or meetings, this tool offers both a simple web user interface and a command-line interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Web UI](#web-ui)
  - [Command Line Interface (CLI)](#command-line-interface-cli)
- [Configuration](#configuration)
- [License](#license)
- [Support](#support)
- [Contribution](#contribution)

## Installation

1. **Clone this repository**:
   
   ```bash
   git clone https://github.com/NeilOrley/Teams-Summarizer.git
   cd Teams-Summarizer
   ```

2. **Install the dependencies**:
   
   Ensure you have Python installed and use the following command to install all necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web UI

To start the web user interface:

```bash
python app.py
```

This will launch a local web server. You can access the application via your browser at `http://localhost:5000`.

### Command Line Interface (CLI)

To use the application via command line:

```bash
python cli_summarize.py --file_path=path_to_vtt_file.vtt
```

### Configuration

For the application to function, you must have an OpenAI API key. Once you have your key, please configure it in the `config.ini` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support

No support is provided for this application. However, you can still open [issues](https://github.com/NeilOrley/Teams-Summarizer/issues) on GitHub if you encounter problems or have suggestions.

## Contribution

Contributions are welcome! Don't hesitate to open pull requests or submit issues on [GitHub](https://github.com/NeilOrley/Teams-Summarizer).

> ---
>
> _Note: This text was generated with the help of ChatGPT, a linguistic model developed by OpenAI._