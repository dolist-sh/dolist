import { useState, useEffect, useContext } from 'react';
import { GlobalContext } from '../contexts/global';

export default function useThemeProps() {
  const globalcontext = useContext(GlobalContext);

  const [logoUri, setLogoUri] = useState<string>(null);
  const [colorThemeIconUri, setcolorThemeIconUri] = useState<string>(null);
  const [addGithubLogoUri, setAddGithubLogoUri] = useState<string>(null);
  const [githubLogoUri, setGithubLogoUri] = useState<string>(null);
  const [settingIconUri, setSettingIconUri] = useState<string>(null);
  const [logoutIconUri, setLogoutIconUri] = useState<string>(null);

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

  return {
    logoUri,
    theme: globalcontext.theme,
    addGithubLogoUri,
    githubLogoUri,
    colorThemeIconUri,
    changeColorThemeHandler,
    settingIconUri,
    logoutIconUri,
  };
}
