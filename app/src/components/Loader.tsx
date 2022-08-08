import * as React from 'react';
import { CSSProperties } from 'react';
import PanmanLoader from 'react-spinners/PacmanLoader';

interface LoaderProps {
  loaderColor: string;
}

const Loader: React.FC<LoaderProps> = ({ loaderColor }: LoaderProps) => {
  const override: CSSProperties = {
    display: 'block',
    margin: '0 auto',
  };

  return (
    <>
      <PanmanLoader loading={true} size={30} color={loaderColor} cssOverride={override} />
    </>
  );
};

export default Loader;
