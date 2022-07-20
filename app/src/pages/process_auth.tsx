import React, { useEffect } from 'react';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';

const ProcessAuthPage: NextPage = () => {
  const { query } = useRouter();

  useEffect(() => {
    console.log('Effect hook called');
    const redirect = query.redirect;
    const tempCode = query.code;

    if (redirect && tempCode) {
      const fetchAccessCode = async (sessionCode: string) => {
        //TOOD: Call the auth handling proxy at our own backend: https://stackoverflow.com/questions/43262121/trying-to-use-fetch-and-pass-in-mode-no-cors

        const clientId = process.env.GITHUB_OAUTH_CLIENT_ID;
        const clientSecret = process.env.GITHUB_OAUTH_CLIENT_SECRET;
        const confirmUri = process.env.GITHUB_OAUTH_CONFIRM_URI;

        const response = await fetch(
          `https://github.com/login/oauth/access_token?client_id=${clientId}&client_secret=${clientSecret}&redirect_uri=${confirmUri}&code=${sessionCode}`,
          {
            method: 'POST',
            mode: 'no-cors',
            headers: {
              'Content-Type': 'application/json',
              Accept: 'application/json',
            },
          },
        );

        return response;
      };

      fetchAccessCode(tempCode as string).then((data) => console.log(data));
    }
  }, [query]);

  return (
    <div className="flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="flex flex-row justify-center align-middle">
        <p>{'Process Auth'}</p>
      </div>
    </div>
  );
};

export default ProcessAuthPage;
