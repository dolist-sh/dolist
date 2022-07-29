import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import type { NextPage } from 'next';

import { RepoCard } from '../components';
import { getUserRepos } from '../api';
import { Repo } from '../types';

const AppMainPage: NextPage = () => {
  const [repos, setRepos] = useState([]);
  const { push } = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');

    !token ? push('/signin') : null;

    getUserRepos(token).then((data) => {
      const repos: Repo[] = data.map((repo) => {
        return {
          id: repo.id,
          name: repo.name,
          fullName: repo.full_name,
          defaultBranch: repo.default_branch,
          url: repo.url,
          language: repo.language,
          visibility: repo.visibility,
        };
      });
      setRepos(repos);
    });
  }, []);

  return (
    <div className="flex flex-col w-11/12 h-screen m-auto mt-10">
      <div className="flex flex-row justify-center align-middle">
        <p>{'App Main Page'}</p>
      </div>
      <div className="flex flex-col">
        {repos.map((repo) => (
          <RepoCard key={repo.id} name={repo.name} fullName={repo.fullName} branch={repo.defaultBranch} />
        ))}
      </div>
    </div>
  );
};

export default AppMainPage;
