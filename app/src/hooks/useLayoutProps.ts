import { useState, useEffect } from 'react';
import { IGlobalContext } from '../contexts/global';

export default function useLayoutProps(context: IGlobalContext) {
  const [logoUri, setLogoUri] = useState<string>(null);
  const [colorThemeIconUri, setcolorThemeIconUri] = useState<string>(null);
  const [addGithubLogoUri, setAddGithubLogoUri] = useState<string>(null);
  const [githubLogoUri, setGithubLogoUri] = useState<string>(null);
  const [settingIconUri, setSettingIconUri] = useState<string>(null);
  const [logoutIconUri, setLogoutIconUri] = useState<string>(null);

  useEffect(() => {
    if (context.theme === 'dark') {
      setLogoUri('/images/logo_dark_multiline.png');
      setcolorThemeIconUri('/images/lightmode_cream.png');
      setGithubLogoUri('/images/github_white.png');
      setAddGithubLogoUri('/images/add_github_white.png');
      setLogoutIconUri('/images/logout_light.png');
      setSettingIconUri('/images/settings_light.png');
    }
    if (context.theme === 'light') {
      setLogoUri('/images/logo_light_multiline.png');
      setcolorThemeIconUri('/images/nightmode.png');
      setGithubLogoUri('/images/github_black.png');
      setAddGithubLogoUri('/images/add_github_black.png');
      setLogoutIconUri('/images/logout_dark.png');
      setSettingIconUri('/images/settings_dark.png');
    }
  }, [context.theme]);

  const changeColorThemeHandler = (event: React.MouseEvent) => {
    event.preventDefault();

    if (context.theme === 'dark') {
      context.switchToLight();
    }

    if (context.theme === 'light') {
      context.switchToDark();
    }
  };

  const logoutHandler = (event: React.MouseEvent) => {
    event.preventDefault();
    localStorage.removeItem('token');
    window.location.assign('/signin');
  };

  return {
    logoUri,
    theme: context.theme,
    addGithubLogoUri,
    githubLogoUri,
    colorThemeIconUri,
    changeColorThemeHandler,
    logoutHandler,
    settingIconUri,
    logoutIconUri,
  };
}
