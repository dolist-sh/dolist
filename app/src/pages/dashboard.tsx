import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../contexts/global';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Layout, AddRepoModal, RepoOverview } from '../components';

const DashboardPage: NextPage = () => {
  const { push } = useRouter();

  const globalcontext = useContext(GlobalContext);

  const [logoUri, setLogoUri] = useState(null);
  const [colorThemeIconUri, setcolorThemeIconUri] = useState(null);
  const [addGithubLogoUri, setAddGithubLogoUri] = useState(null);
  const [githubLogoUri, setGithubLogoUri] = useState(null);
  const [settingIconUri, setSettingIconUri] = useState(null);
  const [logoutIconUri, setLogoutIconUri] = useState(null);
  const [modalOpenCounter, setModalOpenCounter] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem('token');
    !token ? push('/signin') : null;
  }, []);

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setLogoUri('/images/logo_dark_multiline.png');
      setcolorThemeIconUri('/images/lightmode_cream.png');
      setGithubLogoUri('/images/github_white.png');
      setAddGithubLogoUri('/images/add_github_white.png');
      setLogoutIconUri('/images/logout_light.png');
      setSettingIconUri('/images/settings_light.png');
    }
    if (globalcontext.theme === 'light') {
      setLogoUri('/images/logo_light_multiline.png');
      setcolorThemeIconUri('/images/nightmode.png');
      setGithubLogoUri('/images/github_black.png');
      setAddGithubLogoUri('/images/add_github_black.png');
      setLogoutIconUri('/images/logout_dark.png');
      setSettingIconUri('/images/settings_dark.png');
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

  const logoutHandler = (event: React.MouseEvent) => {
    event.preventDefault();

    localStorage.removeItem('token');
    window.location.assign('/signin');
  };

  const modalOpenHandler = (event: React.MouseEvent) => {
    event.preventDefault();
    const counter = modalOpenCounter + 1;
    setModalOpenCounter(counter);
  };

  const layoutProps = {
    logoUri,
    theme: globalcontext.theme,
    colorThemeIconUri,
    changeColorThemeHandler,
    settingIconUri,
    logoutIconUri,
    logoutHandler,
  };

  return (
    <Layout {...layoutProps}>
      <AddRepoModal githubLogoUri={githubLogoUri} openCounter={modalOpenCounter} />
      <div className="w-full h-1/4 pt-10 pb-5">
        <div className="w-5/6 h-full m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Start monitoring the repositories`}</h2>
          <div className="flex flex-row h-auto mt-5 ml-3 justify-start z-10">
            <button
              type="button"
              onClick={modalOpenHandler}
              className="flex flex-col w-[30%] h-full p-5 pt-7 pb-7 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-dashed border-black dark:border-dolist-cream rounded"
            >
              <div className="flex flex-col w-1/4 h-1/4 m-auto">
                <img src={addGithubLogoUri} className="w-7 h-7 ml-2 self-center" />
              </div>
              <p className="font-std font-bold text-xs text-black dark:text-dolist-cream pt-3">{`Monitor GitHub Repo`}</p>
            </button>
          </div>
        </div>
      </div>
      <div className="w-full h-3/4 pt-10 pb-5">
        <div className="w-5/6 min-h-full h-auto m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Monitored repositroies`}</h2>
          <div className="flex flex-row h-auto mt-5 mb-5 ml-3 justify-evenly">
            <RepoOverview githubLogoUri={githubLogoUri} />
            <RepoOverview githubLogoUri={githubLogoUri} />
            <RepoOverview githubLogoUri={githubLogoUri} />
          </div>
          <div className="flex flex-row h-auto mt-5 mb-5 ml-3 justify-evenly">
            <RepoOverview githubLogoUri={githubLogoUri} />
            <RepoOverview githubLogoUri={githubLogoUri} />
            <RepoOverview githubLogoUri={githubLogoUri} />
          </div>
          <div className="flex flex-row h-auto mt-5 mb-5 ml-3 justify-evenly">
            <RepoOverview githubLogoUri={githubLogoUri} />
            <RepoOverview githubLogoUri={githubLogoUri} />
            <RepoOverview githubLogoUri={githubLogoUri} />
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
