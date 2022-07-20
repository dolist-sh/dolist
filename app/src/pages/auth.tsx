import React from 'react';
import type { NextPage } from 'next';

const AuthPage: NextPage = () => {
  const client_id = process.env.GITHUB_OAUTH_CLIENT_ID;
  const redirect_uri = process.env.GITHUB_OAUTH_REDIRECT_URI;

  return (
    <div className="flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="flex flex-row justify-center align-middle">
        <button className=" px-3 py-2 border-2 text-sm border-dolist-darkblue rounded" type="button">
          <a href={`https://github.com/login/oauth/authorize/?client_id=${client_id}&redirect_uri=${redirect_uri}`}>
            {'Auth with Github'}
          </a>
        </button>
      </div>
    </div>
  );
};

export default AuthPage;
