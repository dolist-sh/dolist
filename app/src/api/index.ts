//TODO: Add return data type
export const getUser = async (token: string) => {
  const response = await fetch(`http://localhost:8000/user`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};

export const getAuthCode = async (sessionCode: string): Promise<string | null> => {
  const response = await fetch(`http://localhost:8000/auth?session_code=${sessionCode}`, {
    method: 'POST',
    mode: 'cors',
  });

  if (response.status === 200) {
    return response.json();
  }

  return null;
};

export const getUserRepos = async (token: string) => {
  const response = await fetch(`http://localhost:8000/user/repos`, {
    method: 'GET',
    mode: 'cors',
    headers: { Authorization: `token ${token}` },
  });
  return response.json();
};
