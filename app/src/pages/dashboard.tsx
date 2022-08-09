import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../contexts/global';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { ColorThemeBtn } from '../components';

interface RepoOverviewProps {
  githubLogoUri: string;
}

const RepoOverview: React.FC<RepoOverviewProps> = ({ githubLogoUri }: RepoOverviewProps) => {
  return (
    <div className="flex flex-col w-[30%] h-full p-3 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-dashed border-black dark:border-dolist-cream rounded">
      <div className="flex flex-row w-full h-1/4 justify-evenly">
        <div className="flex flex-row w-1/2">
          <img src={githubLogoUri} className="w-7 h-7 self-center mr-1" />
          <div className="flex flex-col">
            <h4 className="font-std font-bold text-[12px] text-black dark:text-dolist-cream">{`whathecker/api`}</h4>
            <p className="font-std font-bold text-[8.5px] text-dolist-gray dark:text-dolist-cream">
              {`branch: `}
              <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">{`main`}</span>
            </p>
          </div>
        </div>
        <div className="w-1/2 mt-1">
          <p className="text-[8.5px] font-std font-bold text-right text-dolist-gray dark:text-dolist-cream">
            {`from last commit: `}
            <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">{`694949`}</span>
          </p>
        </div>
      </div>
      <div className="flex flex-col pt-5 ml-2 mr-2">
        <h4 className="font-std font-bold text-dolist-gray dark:text-dolist-cream text-[11px]">{`To-Do Report`}</h4>
        <div className="flex flex-row mt-2 justify-between ml-1 mr-1">
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Total`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`20`}</p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`New`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`2`}</p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Resolved`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`3`}</p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Old`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`15`}</p>
          </div>
        </div>
      </div>
      <div className="flex flex-row pt-5 ml-2 mr-2 justify-evenly">
        <a className="w-1/2 font-std font-bold text-[10px] text-dolist-darkblue dark:text-white underline">{`view full report`}</a>
        <p className="w-1/2 font-std font-bold text-[10px] text-dolist-gray dark:text-white text-right">
          {`updated at: `}
          <span className="font-std text-[10px] text-dolist-lightgray dark:text-dolist-cream">{`--`}</span>
        </p>
      </div>
    </div>
  );
};

const DashboardPage: NextPage = () => {
  const { push } = useRouter();

  const globalcontext = useContext(GlobalContext);

  const [logoUri, setLogoUri] = useState(null);
  const [colorThemeIconUri, setcolorThemeIconUri] = useState(null);
  const [addGithubLogoUri, setAddGithubLogoUri] = useState(null);
  const [githubLogoUri, setGithubLogoUri] = useState(null);
  const [settingIconUri, setSettingIconUri] = useState(null);
  const [logoutIconUri, setLogoutIconUri] = useState(null);

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

  // TODO: Wrap the page structure with Layout component
  return (
    <div className="flex flex-col w-full min-h-screen h-auto overflow-hidden justify-start content-center">
      <div className="fixed w-full h-[85px] border-b-[0.5px] border-dolist-lightgray dark:border-dolist-cream z-40">
        <header className="flex flex-row bg-dolist-bg-light dark:bg-dolist-bg-dark w-5/6 h-full m-auto mt-0 mb-0 p-2 justify-between">
          <a className="cursor-pointer">
            <img src={logoUri} className="w-16 h-16" />
          </a>
          <div className="w-auto flex flex-row self-center">
            <div className="self-center">
              <ColorThemeBtn
                currentTheme={globalcontext.theme as string}
                colorThemeIconUri={colorThemeIconUri}
                clickHandler={changeColorThemeHandler}
              />
            </div>
            <img src="/images/profile.jpeg" className="w-10 h-10 rounded-full ml-12 self-center" />
            <span className="self-center pl-5 cursor-pointer">
              <img src={settingIconUri} className="w-6 h-6" />
            </span>
            <span className="self-center pl-3 cursor-pointer">
              <img onClick={logoutHandler} src={logoutIconUri} className="w-6 h-6" />
            </span>
          </div>
        </header>
      </div>
      <div className="w-full mt-[85px] pt-5 pb-5 overflow-y-auto">
        <div className="w-full h-1/4 pt-10 pb-5">
          <div className="w-5/6 h-full m-auto mt-0 mb-0">
            <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Start monitoring the repositories`}</h2>
            <div className="flex flex-row h-auto mt-5 ml-3 justify-start z-10">
              <button className="flex flex-col w-[30%] h-full p-5 pt-7 pb-7 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-dashed border-black dark:border-dolist-cream rounded">
                <div className="flex flex-col w-1/4 h-1/4 m-auto z-10">
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
      </div>
    </div>
  );
};

export default DashboardPage;
