import React, { useState, useEffect } from 'react';
import type { NextPage } from 'next';
import { getUserRepos } from '../api';
import { Repo } from '../types';

const AppMainPage: NextPage = () => {
  const [repos, setRepos] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');

    getUserRepos(token).then((data) => {
      const repos: Repo[] = data.map((repo) => {
        return {
          id: repo.id,
          name: repo.name,
          defaultBranch: repo.default_branch,
          url: repo.url,
          language: repo.language,
        };
      });
      setRepos(repos);
    });
  }, []);

  console.log(repos);

  return (
    <div className="flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="flex flex-row justify-center align-middle">
        <p>{'App Main Page'}</p>
      </div>
    </div>
  );
};

export default AppMainPage;
