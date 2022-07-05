# About this project
This is a boilerplate of React application with my preferred stacks, optimized for future reuse when starting a new project.

## How to use this repo
1. `git clone {this repo}`
2. `npm install or yarn`
3. `yarn dev (or yarn start if you want to create production optimized build`
4. `visit localhost:3000`

## Stacks
- This project is a server side rendered React app which uses [NextJS](https://github.com/vercel/next.js)
- Written in [TypeScript](https://github.com/microsoft/TypeScript)
- Uses [styled-component](https://github.com/styled-components) for styling 
- [material-ui](https://github.com/mui-org/material-ui) is used in combination with regular components
- Uses [jest](https://jestjs.io/en/) and [enzyme](https://enzymejs.github.io/enzyme/) for test

## styled-component and material-ui being used together
When styled-component and material-ui are used together in NextJS, it requires [additional setup](https://stackoverflow.com/questions/55109497/how-to-integrate-nextjs-styled-components-with-material-ui). This is implemented in **_document.tsx** file in source code.


