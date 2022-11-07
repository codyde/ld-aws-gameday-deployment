
module.exports = {
  env: {
    NEXT_PUBLIC_LD_CLIENT_KEY: process.env.NEXT_PUBLIC_LD_CLIENT_KEY,
    NEXT_PUBLIC_TEAM_ID: process.env.NEXT_PUBLIC_TEAM_ID
  },
  reactStrictMode: false,
  images: {
    loader: "imgix",
    path: "https://noop/",
  },
  
};
