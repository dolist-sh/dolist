import * as React from 'react';

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
      <a href={oauthUri} className="pl-4 text-xs text-black dark:text-white font-std font-bold">
        {'Continue with Github'}
      </a>
    </button>
  );
};

export default GithubAuthBtn;
