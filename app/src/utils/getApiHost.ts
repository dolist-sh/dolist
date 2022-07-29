export function getApiHost(): string {
  const env = process.env.ENV;

  if (!env) {
    throw new Error('ENV variable is not set');
  }

  let host;

  switch (env) {
    case 'local':
      host = 'http://localhost:8080';
      break;
    case 'local-docker':
      host = 'http://localhost/api';
      break;
    case 'dev':
      host = 'http://15.188.137.121/api';
      break;
  }

  return host;
}
