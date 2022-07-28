export function getApiHost() {
  const isDocker = process.env.RUN_DOCKER;

  if (isDocker) {
    return 'http://server';
  }

  return 'http://localhost:8000';
}
