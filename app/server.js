const next = require('next');
const routes = require('./routes');
const app = next({ dev: process.env.NODE_ENV !== 'production' });
const handler = routes.getRequestHandler(app);
const { createServer } = require('http');

let port = process.env.PORT || 3000;
const env = process.env.NODE_ENV;

app.prepare().then(() => {
    createServer(handler).listen(port, () => {
        console.log(`Next app is running on ${env} enviornment, port number ${port} `);
    });
});
