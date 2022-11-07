import React, { useEffect } from "react";
import SyntaxHighlighter from 'react-syntax-highlighter';
import { a11yDark } from 'react-syntax-highlighter/dist/cjs/styles/hljs';
import ls from 'local-storage';



export default function Modal(code) {
  const [showModal, setShowModal] = React.useState(false);
  const [query, setQuery] = React.useState()
  const [userkey, setuserkey] = React.useState("anonymous")

  async function setID(){
    let id = ls.get('LD_User_Key');
    setuserkey(id)
    return id
  }

  const debugData = [{
    id: "1",
    data: "DEBUG-EMPTY",
  },
  {
    id: "2",
    data: "DEBUG-ALSO-EMPTY",
  }]
  

  useEffect(() => {
    console.log("update to key detected")
  }, [userkey])

  console.log(code.dbDetails)

    async function queryDB() {
        let id = await setID()
        const response = await fetch( window.location.protocol +
          "//" +
          window.location.host +
          "/datas")
        if (response.status != 200) {
          const data = debugData
          setQuery(data)
          return data
        } else {
        const data = await response.text()
        setQuery(data)
        return data
      }
    }

    React.useEffect(() => {
        queryDB();
        console.log("running useeffect")
    },[code.dbDetails])
  
  return (
    <>
      <button
        className="bg-ldyellow text-black uppercase text-sm px-6 py-3 ease-linear transition-all duration-150"
        type="button"
        onClick={() => setShowModal(true)}
      >
        Database Details
      </button>
      {showModal ? (
        <>
          <div
            className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none"
          >
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              {/*content*/}
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-ldgray outline-none focus:outline-none">
                {/*header*/}
                <div className="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t">
                  <h3 className="text-3xl text-white font-semibold">
                    Database Results
                  </h3>
                  <button
                    className="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                    onClick={() => setShowModal(false)}
                  >
                    <span className="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">
                      ×
                    </span>
                  </button>
                </div>
                {/*body*/}
                <div className="relative p-6 flex-auto">
                  <SyntaxHighlighter language="json" style={a11yDark}>
                      {query}
                  </SyntaxHighlighter>
                </div>
                {/*footer*/}
                <div className="flex items-center justify-end p-6 border-t border-solid border-slate-200 rounded-b">
                  <button
                    className="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                    type="button"
                    onClick={() => setShowModal(false)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
        </>
      ) : null}
    </>
  );
}