import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../contexts/global';
import { GithubAuthBtn } from '../components';
import type { NextPage } from 'next';

const ColorThemeBtn: React.FC = () => {
  const globalcontext = useContext(GlobalContext);
  const [iconUri, setIconUri] = useState(null);

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setIconUri('/images/lightmode_cream.png');
    }

    if (globalcontext.theme === 'light') {
      setIconUri('/images/nightmode.png');
    }
  }, [globalcontext.theme]);

  const clickHandler = (event: React.MouseEvent) => {
    event.preventDefault();

    if (globalcontext.theme === 'dark') {
      setIconUri('/images/nightmode.png');
      globalcontext.switchToLight();
    }

    if (globalcontext.theme === 'light') {
      setIconUri('/images/lightmode_cream.png');
      globalcontext.switchToDark();
    }
  };

  return (
    <button
      onClick={clickHandler}
      className="inline-flex w-[120px] h-[35px] bg-dolist-cream dark:bg-dolist-darkblue text-sm border-dolist-darkblue dark:border-dolist-cream border-2 rounded-md justify-center items-center"
    >
      <p className="pr-2 text-xs text-dolist-darkblue dark:text-dolist-cream font-std font-bold">
        {globalcontext.theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
      </p>
      <img src={iconUri} className="w-[12px] h-[12px]" />
    </button>
  );
};

const AuthPage: NextPage = () => {
  const globalcontext = useContext(GlobalContext);

  const [logoUri, setLogoUri] = useState(null);
  const [githubLogoUri, setGithubLogoUri] = useState(null);

  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  const redirectUri = process.env.GITHUB_OAUTH_REDIRECT_URI;
  const oauthUri = `https://github.com/login/oauth/authorize/?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo read:user user:email`;

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setLogoUri('/images/logo_dark_multiline.png');
      setGithubLogoUri('/images/github_white.png');
    }
    if (globalcontext.theme === 'light') {
      setLogoUri('/images/logo_light_multiline.png');
      setGithubLogoUri('/images/github_black.png');
    }
  }, [globalcontext.theme]);

  // TODO: Use next/router for redirect upon clicking the button instead of href on the anchor tag

  return (
    <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark flex flex-col h-screen">
      <div className="flex flex-row justify-end content-start mt-6 mr-14">
        <ColorThemeBtn />
      </div>
      <div className="flex flex-col justify-center w-11/12  m-auto">
        <div className="flex flex-row justify-center align-middle">
          {logoUri ? <img src={logoUri} className="w-24 h-24" /> : null}
        </div>
        <div className="flex flex-row justify-center align-middle mt-8 mb-8">
          <h1 className="text-black dark:text-dolist-cream font-std font-bold">{`Monitor TODOs & technical debts with dolist.sh`}</h1>
        </div>
        <div className="flex flex-row justify-center align-middle">
          {githubLogoUri ? <GithubAuthBtn logoUri={githubLogoUri} oauthUri={oauthUri} /> : null}
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
