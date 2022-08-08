import React, { useEffect, useState } from 'react';
import type { NextPage } from 'next';

interface GithubAuthBtnProps {
  oauthUri: string;
  logoUri: string;
}

const GithubAuthBtn: React.FC<GithubAuthBtnProps> = ({ oauthUri, logoUri }: GithubAuthBtnProps) => {
  return (
    <button
      className="inline-flex w-[220px] h-[45px] px-3 py-2 bg-dolist-cream dark:bg-dolist-darkblue border text-sm border-black dark:border-dolist-cream rounded  justify-center items-center"
      type="button"
    >
      <img src={logoUri} alt="github_logo_black_color" className="w-[28px] h-[28px]" />
      {/** TODO: change this to p tag when click handler is implemented */}
      <a href={oauthUri} className="pl-4 text-xs text-black dark:text-white font-bold">
        {'Continue with Github'}
      </a>
    </button>
  );
};

const AuthPage: NextPage = () => {
  const [logoUri, setLogoUri] = useState(null);
  const [githubLogoUri, setGithubLogoUri] = useState(null);

  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  const redirectUri = process.env.GITHUB_OAUTH_REDIRECT_URI;
  const oauthUri = `https://github.com/login/oauth/authorize/?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo read:user user:email`;

  useEffect(() => {
    if (localStorage.getItem('theme') === 'dark') {
      setLogoUri('/images/logo_dark_multiline.png');
      setGithubLogoUri('/images/github_white.png');
    } else {
      setLogoUri('/images/logo_light_multiline.png');
      setGithubLogoUri('/images/github_black.png');
    }
  }, []);

  // TODO: Use next/router for redirect upon clicking the button instead of href on the anchor tag

  return (
    <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark flex flex-col h-screen">
      <div className="flex flex-row justify-end content-start mt-6 mr-14">
        {/** TODO: color theme button should be a separate component */}
        <button className="inline-flex w-[120px] h-[35px] text-sm bg-dolist-cream border-2 border-dolist-darkblue rounded-md justify-center items-center">
          <p className="pr-2 text-xs font-bold">{`Dark Mode`}</p>
          <img src="/images/night-mode.png" alt="light_mode_icon_sun" className="w-[12px] h-[12px]" />
        </button>
      </div>
      <div className="flex flex-col justify-center w-11/12  m-auto">
        <div className="flex flex-row justify-center align-middle">
          {logoUri ? <img src={logoUri} className="w-24 h-24" /> : null}
        </div>
        <div className="flex flex-row justify-center align-middle mt-8 mb-8">
          <h1 className="text-black dark:text-dolist-cream font-bold">{`Monitor TODOs & technical debts with dolist.sh`}</h1>
        </div>
        <div className="flex flex-row justify-center align-middle">
          {githubLogoUri ? <GithubAuthBtn logoUri={githubLogoUri} oauthUri={oauthUri} /> : null}
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
