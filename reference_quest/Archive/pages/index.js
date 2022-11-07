import React, { useState } from "react";
import Head from "next/head";
import Loginbox from "../components/loginbox.js";
import Connection from "../components/connection.js";
import "semantic-ui-css/semantic.min.css";
import { useFlags } from "launchdarkly-react-client-sdk";
import toast, { Toaster } from "react-hot-toast";
import Banner from "../components/banner.js";
import Preview from "../components/preview.js";
import Herotext from "../components/herotext.js";
import Grid from "../components/grid.js";


export default function Home() {
  // Feature flags that are created and managed in LaunchDarkly
  const { siteRelease, logMode } = useFlags();
  const [userObj, setUserObj] = useState(); 
  //
  return (
    <div className="h-screen bg-ld-ls bg-no-repeat bg-center bg-cover">
      <Head>
        <title>UnicornRentals</title>
        <meta name="description" content="Built for exploring LaunchDarkly" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Toaster
        position="bottom-center"
        reverseOrder={false}
        gutter={8}
        containerClassName=""
        containerStyle={{}}
        toastOptions={{
          className: "",
          duration: 5000,
          style: {
            background: "#00000",
            color: "#fffff",
          },
          success: {
            icon: "🚀",
            style: {
              fontSize: 22,
              background: "#282828",
              color: "white",
            },
          },
          error: {
            icon: "⚠️",
            style: {
              fontSize: 22,
              background: "#FF386B",
              color: "white",
            },
          },
        }}
      />
      {/* 
        ### DEV NOTES ###
        Our feature flag for the big release is below. Ensure it's been created in LaunchDarkly. 

        Flag Name/Key - siteRelease
        Flag Type - Boolean
      
      */}
      {siteRelease ? 
      <main className="h-screen grid grid-cols-4 grid-rows-3">
          <div className="grid col-span-4 row-start-3 my-8 lg:row-start-2 lg:col-span-1 lg:col-start-1 justify-center items-center px-8">
            <Loginbox userObj={userObj} setUserObj={setUserObj} />
          </div>
        <div className="grid col-span-4 row-start-1  h-2/3 items-center">
          <Banner />
        </div>
        <div className="grid col-start-2 col-span-3 row-start-2 items-center ">
            <Herotext />
        </div>
        <div className="grid col-span-4 row-start-2 lg:col-start-2 lg:col-span-3 lg:row-start-3 justify-center items-center lg:w-full">
            <Grid userObj={userObj} />
        </div>
        {/* 
        
        ### DEV NOTES ###

        We can hide components behind a feature flag, and use targeting rules to control which users can see them - like a debug menu for a database connection
        
        Debug mode feature flag is below. Ensure it's been created in LaunchDarkly. This is a multi-variate string. This means you can create multiple version of this flag that return different results. 
        
        Flag Name/Key - logMode
        Flag Type - String
        On value - 'debug'
        Off value - 'default'

        */}
        {logMode == 'debug' ? (
          <div className="grid col-span-4 row-start-2 lg:col-start-1 lg:col-span-1 lg:row-start-3 justify-center items-center lg:w-full">
            <Connection />
          </div>
        ) : null}
      </main> : 
        <main className="h-screen bg-ld-ls grid grid-cols-4 grid-rows-3">
          <div className="grid col-span-4 row-start-2 items-center ">
            <Preview />
          </div> 
        </main>
      }
    </div>
  );
}
