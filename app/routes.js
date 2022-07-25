const routes = require('next-routes');

module.exports = routes()
.add('/', 'main')
.add('/signin', 'auth')
.add('/process_auth', 'process_auth')
.add('/tasklist', 'tasklist')

