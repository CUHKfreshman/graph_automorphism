# AutoViz
The project is run on Vue 3 + Flask + Redis. The recommended package manager is *yarn* which has better support for Vue.\\
You may need the following commands to run the application:
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
python3 app.py
```

## Project development

### Current status
1. Basic graph analyzer:
    1. Graph rendering: Done
    2. Metrics report: Not yet (Choosing layout)
    3. Layout Options: Done
    4. Modular Self-Assembling UI: Done (But may need to modify)
2. SSM graph analyzer:
    1. Basic color mapping: Done
    2. Metrics report: Not yet
    3. Modified node-wise operations: Not yet
3. AutoTree Analyzer:
    1. AutoTree graph rendering: Done
    2. Metrics report: Not yet
    3. Modified node-wise operations: Not yet
4. IM graph analyzer:
   1. Basic color mapping: Done
   2. Metrics report: Not yet
   3. Modified node-wise operations: Not yet
   4. Step-by-step visualization: Done
   5. K-neighbor visualization: K button not assigned
   6. Two seed set comparison: Not yet

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
