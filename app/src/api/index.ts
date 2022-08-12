//TODO: Add return data type

import { getApiHost } from '../utils';

export const getUser = async (token: string) => {
  const host = getApiHost();

  const response = await fetch(`${host}/user`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};

export const getAuthCode = async (sessionCode: string): Promise<string | null> => {
  const host = getApiHost();

  const response = await fetch(`${host}/auth?session_code=${sessionCode}`, {
    method: 'GET',
    mode: 'cors',
  });

  if (response.status === 200) {
    return response.json();
  }

  return null;
};

export const getGithubRepos = async (token: string) => {
  const host = getApiHost();

  const response = await fetch(`${host}/user/repos`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};

export const getRepoTasks = async (token: string, repoFullName: string, branch: string) => {
  const host = getApiHost();

  const response = await fetch(`${host}/repo/tasks?repo_name=${repoFullName}&branch=${branch}`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};

export const postMonitoredRepos = async (token: string) => {
  const host = getApiHost();

  const response = await fetch(`${host}/user/monitoredrepo`, {
    method: 'POST',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
    body: JSON.stringify({
      repos: [
        { fullName: 'whathecker/api', provider: 'github' },
        { fullName: 'whathecker/api', provider: 'github' },
      ],
    }),
  });
  return response.json();
};
