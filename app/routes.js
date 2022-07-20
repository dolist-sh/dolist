const routes = require('next-routes');

module.exports = routes()
.add('/', 'auth')
.add('/process_auth', 'process_auth')



