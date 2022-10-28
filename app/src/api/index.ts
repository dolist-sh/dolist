//TODO: Add return data type
import { MonitoredRepo, Repo } from '../types';
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

export const getMonitoredRepos = async (token: string): Promise<MonitoredRepo[]> => {
  const host = getApiHost();

  const response = await fetch(`${host}/monitoredrepos`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};

export const getMonitoredRepo = async (token: string, mrepoId: string): Promise<MonitoredRepo> => {
  const host = getApiHost();

  const response = await fetch(`${host}/monitoredrepos/${mrepoId}`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};

export const postMonitoredRepos = async (token: string, repos: Repo[]) => {
  const host = getApiHost();

  const response = await fetch(`${host}/monitoredrepos`, {
    method: 'POST',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
    body: JSON.stringify({
      repos: repos,
    }),
  });
  return response.json();
};
