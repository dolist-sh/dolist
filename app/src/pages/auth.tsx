import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../contexts/global';
import { GithubAuthBtn, ColorThemeBtn } from '../components';
import type { NextPage } from 'next';

const AuthPage: NextPage = () => {
  const globalcontext = useContext(GlobalContext);

  const [logoUri, setLogoUri] = useState(null);
  const [githubLogoUri, setGithubLogoUri] = useState(null);
  const [colorThemeIconUri, setcolorThemeIconUri] = useState(null);

  const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
  const redirectUri = process.env.GITHUB_OAUTH_REDIRECT_URI;
  const oauthUri = `https://github.com/login/oauth/authorize/?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo read:user user:email`;

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setLogoUri('/images/logo_dark_multiline.png');
      setGithubLogoUri('/images/github_white.png');
      setcolorThemeIconUri('/images/lightmode_cream.png');
    }
    if (globalcontext.theme === 'light') {
      setLogoUri('/images/logo_light_multiline.png');
      setGithubLogoUri('/images/github_black.png');
      setcolorThemeIconUri('/images/nightmode.png');
    }
  }, [globalcontext.theme]);

  const changeColorThemeHandler = (event: React.MouseEvent) => {
    event.preventDefault();

    if (globalcontext.theme === 'dark') {
      globalcontext.switchToLight();
    }

    if (globalcontext.theme === 'light') {
      globalcontext.switchToDark();
    }
  };

  // TODO: Use next/router for redirect upon clicking the button instead of href on the anchor tag

  return (
    <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark flex flex-col h-screen">
      <div className="flex flex-row justify-end content-start mt-6 mr-14">
        <ColorThemeBtn
          currentTheme={globalcontext.theme as string}
          colorThemeIconUri={colorThemeIconUri}
          clickHandler={changeColorThemeHandler}
        />
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
