import React from 'react';
import type { NextPage } from 'next';

const AuthPage: NextPage = () => {
  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  const redirectUri = process.env.GITHUB_OAUTH_REDIRECT_URI;
  const oauthUri = `https://github.com/login/oauth/authorize/?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo read:user user:email`;

  // TODO: Use next/router for redirect upon clicking the button instead of href on the anchor tag

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-row justify-end content-start mt-6 mr-14">
        {/** TODO: color theme button should be a separate component */}
        <button className="inline-flex w-[120px] h-[35px] text-sm bg-dolist-cream border-2 border-dolist-darkblue rounded-md justify-center items-center">
          <p className="pr-2 text-xs font-bold">{`Dark Mode`}</p>
          <img src="/images/night-mode.png" alt="light_mode_icon_sun" className="w-[12px] h-[12px]" />
        </button>
      </div>
      <div className="flex flex-col justify-center w-11/12  m-auto">
        <div className="flex flex-row justify-center align-middle">
          <img src="/images/logo_light_multiline.png" alt="dolist_logo_light" className="w-24 h-24" />
        </div>
        <div className="flex flex-row justify-center align-middle mt-8 mb-8">
          <h1 className="font-bold">{`Monitor TODOs & technical debts with dolist.sh`}</h1>
        </div>
        <div className="flex flex-row justify-center align-middle">
          <button
            className="inline-flex w-[220px] h-[45px] px-3 py-2 bg-dolist-cream  border-2 text-sm border-black rounded  justify-center items-center"
            type="button"
          >
            <img src="/images/github_black.png" alt="github_logo_black_color" className="w-[28px] h-[28px]" />
            {/** TODO: change this to p tag when click handler is implemented */}
            <a href={oauthUri} className="pl-4 text-xs font-bold">
              {'Continue with Github'}
            </a>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
