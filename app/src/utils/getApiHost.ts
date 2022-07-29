export function getApiHost() {
  const isDocker = process.env.RUN_DOCKER;

  if (isDocker) {
    return 'http://localhost/api';
  }

  return 'http://localhost:8080';
}
