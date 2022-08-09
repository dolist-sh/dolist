import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../contexts/global';
import type { NextPage } from 'next';
import { ColorThemeBtn } from '../components';

const DashboardPage: NextPage = () => {
  const globalcontext = useContext(GlobalContext);

  const [logoUri, setLogoUri] = useState(null);
  const [colorThemeIconUri, setcolorThemeIconUri] = useState(null);
  const [settingIconUri, setSettingIconUri] = useState(null);
  const [logoutIconUri, setLogoutIconUri] = useState(null);

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setLogoUri('/images/logo_dark_multiline.png');
      setcolorThemeIconUri('/images/lightmode_cream.png');
      setLogoutIconUri('/images/logout_light.png');
      setSettingIconUri('/images/settings_light.png');
    }
    if (globalcontext.theme === 'light') {
      setLogoUri('/images/logo_light_multiline.png');
      setcolorThemeIconUri('/images/nightmode.png');
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

  return (
    <div className="flex flex-col w-full h-screen justify-start content-center">
      <div className="w-full h-[85px] border-b-[0.5px] border-dolist-lightgray dark:border-dolist-cream">
        <header className="flex flex-row w-5/6 m-auto mt-0 mb-0 p-2 justify-between">
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
            <a className="self-center pl-5 cursor-pointer">
              <img src={settingIconUri} className="w-6 h-6" />
            </a>
            <a className="self-center pl-3 cursor-pointer">
              <img src={logoutIconUri} className="w-6 h-6" />
            </a>
          </div>
        </header>
      </div>
      <div className="w-full h-1/4 mt-14 mb-5">
        <div className="w-5/6 h-full m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Start monitoring the repositories`}</h2>
          <div className="flex flex-row h-auto mt-5 justify-evenly border-2">
            <button>{`GH btn`}</button>
            <button>{`GL btn`}</button>
            <button>{`BicBucket BTN`}</button>
          </div>
        </div>
      </div>
      <div className="w-full h-2/4">
        <div className="w-5/6 h-full m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Monitored repositroies`}</h2>
          <div className="flex flex-row h-auto mt-5 justify-evenly border-2">
            <div>{`Repo 1`}</div>
            <div>{`Repo 2`}</div>
            <div>{`Repo 3`}</div>
            <div>{`Repo 4`}</div>
            <div>{`Repo 5`}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
