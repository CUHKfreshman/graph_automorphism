# AutoViz
The project is run on Vue 3 + Flask + Redis. The recommended package manager is *yarn* which has better support for Vue.
## Links
Demo of [version 1 (without newest IM features)](https://fintech.se.cuhk.edu.hk/wp-content/uploads/2023/06/FTEC-FYP-Graph-Automorphism-over-Social-Network-2023-Outstanding-Final-Year-Project-Award.mp4).\
You can also view our paper [here](https://dl.acm.org/doi/abs/10.1007/978-3-031-47843-7_25).
## How to start
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
    1. Graph rendering
    2. Metrics report
    3. Layout Options
    4. Modular Self-Assembling UI
2. SSM graph analyzer: ### Currently Disabled
    1. Basic color mapping
    2. Metrics report
    3. Modified node-wise operations
3. AutoTree Analyzer: ### Currently Disabled
    1. AutoTree graph rendering
    2. Metrics report
    3. Modified node-wise operations
4. IM graph analyzer: ### Currently Disabled
   1. Basic color mapping
   2. Metrics report
   3. Modified node-wise operations
   4. Step-by-step visualization:
   5. K-neighbor visualization
   6. Customizable seed set & config
   7. Integrated Pruning Methods



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
