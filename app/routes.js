const routes = require('next-routes');

module.exports = routes()
.add('/', 'auth')
.add('/process_auth', 'process_auth')
.add('/process_auth/confirm', 'confirm_auth')



