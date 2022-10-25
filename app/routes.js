const routes = require('next-routes');

module.exports = routes()
.add('/', 'dashboard')
.add('/signin', 'auth')
.add('/process_auth', 'process_auth')
.add('/report/[fullname]', 'report')

