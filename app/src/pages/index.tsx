import React from 'react';
import type { NextPage } from 'next';
import { HelloWorld } from '../components/hello-world';

const Homepage: NextPage = () => {
  return (
    <div>
      <HelloWorld />
    </div>
  );
};

export default Homepage;
