import React, { useEffect, useState } from "react";
import ls from "local-storage";

export default function Grids(userObj) {
  async function setID() {
    let id = ls.get("LD_User_Key");
    return id;
  }

  const [dummyData, setDummyData] = useState([]);

  const seedData = [
    {
      "id": 1,
      "title": "Debug Ipsum 1",
      'text': "This is our debug text. Charlie ate the last candy bar.",
    },
    {
      "id": 2,
      "title": "Debug Ipsum 2",
      "text": "We're debugging all the Unicorns. They are trampling our code.",
    },
    {
      "id": 3,
      "title": "Debug Ipsum 3",
      "text": "Will it ever end? Speculation is nay. It likely won't.",
    },
  ];

  useEffect(() => {
    const fetchData = async () => {
      let id = await setID();
      const response = await fetch(
        window.location.protocol +
          "//" +
          window.location.host +
          "/datas"
      );
      if (response.status != 200) {
        setDummyData(seedData);
        return seedData;
      } else {
        const nbdData = await response.json();
        setDummyData(nbdData[0]);
      }
    };
    fetchData();
  }, [userObj]);

  return (
    <div className="grid space-x-4 justify-center invisible sm:invisible md:visible">
      <div className="grid grid-cols-3 col-span-4 space-x-4 justify-center">
        {dummyData.map(function (card) {
          return (
            <div key={card.id}
              className={`mx-auto w-3/4 shadow-2xl bg-ldgray py-3 px-3 text-white`}
            >
              <h1 className="text-2xl sm:text-base xl:text-2xl">
                {card.title}
              </h1>
              <p className="text-ldgraytext text-xl invisible md:text-xl xl:text-xl sm:invisible md:invisible xl:visible">
                {card.text}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
