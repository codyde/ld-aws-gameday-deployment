import React, { useState, useEffect } from "react";
import { useLDClient } from "launchdarkly-react-client-sdk";
import Radium, { StyleRoot } from "radium";
import toast, { Toaster } from "react-hot-toast";
import ls from 'local-storage';

export default function Loginbox({userObj, setUserObj}) {
  const LDClient = useLDClient();

  const [userState, setUserState] = useState({
    username: "",
  });

  async function setCurrLDUser() {
    const obj = await LDClient.getUser();
    return obj;
  }

  const submitUser = async (e) => {
    e.preventDefault();
    const lduser = await setCurrLDUser();
    lduser.key = userState.username;
    await LDClient.identify(lduser);
    const response = await fetch(
      window.location.protocol +
          "//" +
          window.location.host +
          "/login", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(lduser)
          }
    )
    await ls.remove('LD_User_Key')
    await ls.set('LD_User_Key', userState.username)
    LDClient.track('userLogin', { customProperty: userState.username });
    toast.success("Your LaunchDarkly user is " + userState.username);
    setUserObj(userState.username)
    Array.from(document.querySelectorAll("input")).forEach(
      (input) => (input.value = "")
    );
  };

  useEffect(() => {
    setUserState(LDClient.getUser())
  }, [])

  const handleChange = (e) => {
    const { id, value } = e.target;
    setUserState((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  };

  async function setCurrLDUser() {
    const obj = await LDClient.getUser();
    return obj;
  }

  const submitLogout = async (e) => {
    e.preventDefault();
    const lduser = await setCurrLDUser();
    lduser.key = "anonymous";
    await LDClient.identify(lduser);
    await fetch(
      window.location.protocol +
          "//" +
          window.location.host +
          "/logout", {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }
    )
    await ls.remove('LD_User_Key')
    LDClient.track('userClear', { customProperty: userState.username });
    toast.success("User has been cleared");
    Array.from(document.querySelectorAll("input")).forEach(
      (input) => (input.value = "")
    );
  };

  return (
    <StyleRoot>
        <div className="flex justify-center items-center">
        <div className={`bg-ldgray p-4 lg:p-10 lg:px-28 shadow-2xl`}>
          <form>
            <h1 className="text-center text-ldgraytext text-xl lg:text-2xl">
              Login With Your Username
            </h1>
            {/* <p className="mx-auto font-normal text-ldgraytext text-sm lg:text-lg my-6 max-w-lg">
              This login field will create a user object with the LaunchDarkly
              SDK. This user object can be used to interact with targeting
              rules allowing specific feature configurations to be enabled or
              disabled based on users.
            </p> */}
            <div className="mx-auto flex items-center bg-white overflow-hidden px-2 py-1 max-w-lg justify-between">
              <input
                className="text-base text-gray-400 flex-grow outline-none px-2"
                type="input"
                id="username"
                placeholder="Enter Username"
                value={userState.username}
                onChange={handleChange}
              />
              <div className="flex items-center px-2 space-x-4 mx-auto ">
                <button
                  type="submit"
                  className="bg-ldblue text-white text-base px-4 py-2 font-thin"
                  onClick={submitUser.bind(userState)}
                >
                  Submit
                </button>
                </div>
            </div>
            <div className="flex mx-auto m-auto align-middle justify-center py-2 px-4 space-x-4">
               <button
                type="input"
                className="bg-ldred text-white text-base px-2 py-2"
                onClick={submitLogout.bind(userState)}
              >
                Clear Current User
              </button>
              </div>
          </form>
        </div>
      </div>
    </StyleRoot>
  );
}


