# AutoViz
The project is run on Vue 3 + Flask + Redis. The recommended package manager is *yarn* which has better support for Vue.\\
You may need the following commands to run the application:
**For current version, Redis is replaced by long polling. Related code can be safely removed (setup & app.py).**
```
yarn
pip install -r requirement.txt
apt install redis
```
If for general purposes, run
```
./start.sh
```
If debugging is required, run the following commands in different terminals
```
redis-server
yarn dev
python3 ./flask/app.py
```
## Project development

### Current status
1. General Purpose:
    1. Graph rendering: Done
    2. Metrics report: Done
    3. Layout Options: Done
    4. Modular Self-Assembling UI: Done
2. Symmetric Subgraph Matching:
    1. Basic color mapping: Done
    2. Metrics report: Done
    3. Modified node-wise operations: Done
3. AutoTree Analyzer:
    1. AutoTree graph rendering: Done
    2. Metrics report: Done (In SSM)
    3. Modified node-wise operations: Done
4. Influence Maximization:
   1. Basic color mapping: Done
   2. Metrics report: Not yet
   3. Step-by-step visualization: Done
   4. K-neighbor visualization: Done
   5. Customizable seed set & prob: Done

### Remark
For different node-wise operations, should use different entries rather than overriding.


# Default Docs
## Project setup

```
# yarn
yarn

# npm
npm install

# pnpm
pnpm install
```

### Compiles and hot-reloads for development

```
# yarn
yarn dev

# npm
npm run dev

# pnpm
pnpm dev
```

### Compiles and minifies for production

```
# yarn
yarn build

# npm
npm run build

# pnpm
pnpm build
```

### Lints and fixes files

```
# yarn
yarn lint

# npm
npm run lint

# pnpm
pnpm lint
```

### Customize configuration

See [Configuration Reference](https://vitejs.dev/config/).
