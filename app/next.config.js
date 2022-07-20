/** @type {import('next').NextConfig} */

module.exports = {
    reactStrictMode: true,
    env: {
        GITHUB_OAUTH_CLIENT_ID: process.env.GITHUB_OAUTH_CLIENT_ID,
        GITHUB_OAUTH_CLIENT_SECRET: process.env.GITHUB_OAUTH_CLIENT_SECRET,
        GITHUB_OAUTH_REDIRECT_URI: process.env.GITHUB_OAUTH_REDIRECT_URI,
        GITHUB_OAUTH_CONFIRM_URI: process.env.GITHUB_OAUTH_CONFIRM_URI,
    }
}