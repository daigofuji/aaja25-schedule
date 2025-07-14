# AAJA25 Schedule Displayer

Two parts. 
One: Python code that fetches the schedule using guidebook Open API and writes a json file

TLDR: cd to `python` directory and run `python main.py` to get the schedule in `schedule.json`.

Two: React app that reads the json file and displays the schedule in a nice way.

to start develope, type `npm start` in the root directory.


# Python setup. 

I use pyenv to manage my python environment. Used [this set up](https://github.com/BostonGlobe/data-school-closings-scraper?tab=readme-ov-file#setup) and [this blog post](https://medium.com/@miqui.ferrer/the-ultimate-guide-to-managing-python-virtual-environments-in-macos-c8cb49bf0a3c) as reference for setting up the virtual environment.

If necessary, install `Python`, `pyenv`, and `virtualenv` (see link above).

This project uses Python 3.12

```bash
pyenv install 3.12
```

Create a virtualenv for this project. We'll use "AAJA" as the name

```bash
pyenv virtualenv 3.12 AAJA
```
To start developing, you need to activate the environment

```bash
pyenv activate AAJA
pip install -r requirements.txt
```

Runnning the script
```bash
python main.py
```

see memo.md for more details

# Github pages 

To deploy, simply run `npm run deploy` in the root directory. which will push contents of /dist to the `gh-pages` branch.


# Vite + React

This project was made with Node v20.19.0.

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
