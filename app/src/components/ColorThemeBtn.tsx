import * as React from 'react';

interface ColorThemeBtnProps {
  currentTheme: string;
  colorThemeIconUri: string;
  clickHandler: (event: React.MouseEvent) => void;
}

const ColorThemeBtn: React.FC<ColorThemeBtnProps> = ({
  clickHandler,
  colorThemeIconUri,
  currentTheme,
}: ColorThemeBtnProps) => {
  return (
    <button
      onClick={clickHandler}
      className="inline-flex w-[120px] h-[35px] bg-dolist-cream dark:bg-dolist-darkblue text-sm border-dolist-darkblue dark:border-dolist-cream border-2 rounded-md justify-center items-center"
    >
      <p className="pr-2 text-xs text-dolist-darkblue dark:text-dolist-cream font-std font-bold">
        {currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode'}
      </p>
      <img src={colorThemeIconUri} className="w-[12px] h-[12px]" />
    </button>
  );
};

export default ColorThemeBtn;
