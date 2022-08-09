const routes = require('next-routes');

module.exports = routes()
.add('/', 'main')
.add('/dashboard', 'dashboard')
.add('/signin', 'auth')
.add('/process_auth', 'process_auth')
.add('/tasklist', 'tasklist')

