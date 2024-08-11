 useEffect(() => {
    const onscroll = () => {
      const scrolledTo = window.scrollY + window.innerHeight;
      const isReachBottom = document.body.scrollHeight === scrolledTo;
      if (isReachBottom) alert("reached bottom");
    };
    window.addEventListener("scroll", onscroll);
    return () => {
      window.removeEventListener("scroll", onscroll);
    };
  }, []);