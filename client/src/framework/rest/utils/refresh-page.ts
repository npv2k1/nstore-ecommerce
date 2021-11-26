import Router from 'next/router';

//...

export const reload = () => {
  Router.reload(window.location.pathname);
};
