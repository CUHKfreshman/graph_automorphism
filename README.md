# AutoViz
The project is run on Vue 3 + Flask + Redis. The recommended package manager is *yarn* which has better support for Vue.\\
You may need the following commands to run the application:
```
yarn
pip install -r requirement.txt
apt install redis
```
If for general purposes, run below cmd to start the application
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
1. Basic graph analyzer: ### Currently Disabled
    1. Graph rendering: Done
    2. Metrics report: Done
    3. Layout Options: Done
    4. Modular Self-Assembling UI: Done
2. SSM graph analyzer: ### Currently Disabled
    1. Basic color mapping: Done
    2. Metrics report: Done
    3. Modified node-wise operations: Done
3. AutoTree Analyzer: ### Currently Disabled
    1. AutoTree graph rendering: Done
    2. Metrics report: Done
    3. Modified node-wise operations: Done
4. IM graph analyzer: ### Currently Disabled
   1. Basic color mapping: Done
   2. Metrics report: Not yet
   3. Modified node-wise operations: Done
   4. Step-by-step visualization: Done
   5. K-neighbor visualization: Done
   6. Customizable seed set & prob: Done
   7. ***Integrated Pruning Methods: Done



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
