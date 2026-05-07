# INFO3180 VueJS and Flask Starter

This template should help get you started developing with Vue 3 on the frontend and Flask as an API on the backend.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app --debug run
```


Here's exactly what to add to the README.md at the bottom:

```markdown
## Local Setup Instructions

### Prerequisites
- Python 3.x
- Node.js
- PostgreSQL

### Backend Setup
1. Clone the repository
```
git clone -b dev https://github.com/Tramonique/info3180-driftdater.git
cd info3180-driftdater
```

2. Create and activate virtual environment
```
python -m venv venv
.\venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Set up your .env file
```
copy .env.sample .env
```
- Create a local PostgreSQL database called `driftdater`
- Fill in your local PostgreSQL credentials in the DATABASE_URL

5. Run migrations
```
flask db upgrade
```

6. Start the backend
```
flask --app app --debug run
```

### Frontend Setup
Open a new terminal and run:
```
npm install
npm run dev
```

App will be running at http://localhost:5173
```

Paste that at the bottom of the README.md, save it, then commit and push!