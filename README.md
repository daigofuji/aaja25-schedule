# AAJA25 Schedule Displayer

Two parts. 
One: Python code that fetches the schedule using guidebook Open API and writes a json file

TLDR: cd to `python` directory and run `python main.py` to get the schedule in `schedule.json`. you need to have put the `.env` file in the same directory with your [Guidebook API key](https://support.guidebook.com/hc/en-us/articles/360003676094-Guidebook-Open-API).

Two: React app that reads the json file and displays the schedule in a nice way.

To start develope, type `npm start` in the root directory.


# Python setup. 

I use pyenv to manage my python environment. `pyenv` and `virtualenv` via `brew` v3.12 
```bash
brew update
brew install python pyenv pyenv-virtualenv
pyenv install 3.12
pyenv virtualenv 3.12 AAJA
pyenv activate AAJA
pip install -r requirements.txt
```

and [this blog post](https://medium.com/@miqui.ferrer/the-ultimate-guide-to-managing-python-virtual-environments-in-macos-c8cb49bf0a3c) as reference for setting up the virtual environment.

# Python script
The script fetches the schedule from Guidebook Open API and writes it to `schedule.json`.

Running the script
```bash
python main.py
```

See memo.md for more details

# Github pages 

To deploy, simply run `npm run deploy` in the root directory. which will push contents of /dist to the `gh-pages` branch.


**To embed the github page** use following code in your HTML <CODE> part of  file:

```html
<side-chain src="https://daigofuji.github.io/aaja25-schedule/"></side-chain>
<script src="https://apps.npr.org/sidechain/loader.js"></script>
```


# Vite + React

This project was made with Node v20.19.0.

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
