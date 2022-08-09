import * as React from 'react';
import ColorThemeBtn from './ColorThemeBtn';

interface LayoutProps {
  logoUri: string;
  theme: 'light' | 'dark';
  colorThemeIconUri: string;
  changeColorThemeHandler: (e: React.MouseEvent) => void;
  settingIconUri: string;
  logoutIconUri: string;
  logoutHandler: (e: React.MouseEvent) => void;
  children?: React.ReactChild | React.ReactChild[];
}

const Layout: React.FC<LayoutProps> = ({
  logoUri,
  theme,
  colorThemeIconUri,
  settingIconUri,
  logoutIconUri,
  logoutHandler,
  changeColorThemeHandler,
  children,
}: LayoutProps) => {
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
                currentTheme={theme}
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
      <div className="w-full mt-[85px] pt-5 pb-5 overflow-y-auto">{children}</div>
    </div>
  );
};

export default Layout;
