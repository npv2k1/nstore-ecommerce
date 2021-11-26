import { useState } from 'react';
import Cookies from 'js-cookie';
import { useLoginMutation } from '@framework/auth/auth.query';
import { useTranslation } from 'next-i18next';
import { useModalAction } from '@components/ui/modal/modal.context';
import LoginForm from '@components/auth/login-form';
import { useAtom } from 'jotai';
import { authorizationAtom } from '@store/authorization-atom';
import { AUTH_TOKEN } from '@lib/constants';

type FormValues = {
  email: string;
  password: string;
};

const Login = () => {
  const { t } = useTranslation('common');
  const [errorMessage, setErrorMessage] = useState('');
  const [_, authorize] = useAtom(authorizationAtom);
  const { closeModal } = useModalAction();
  const { mutate: login, isLoading: loading } = useLoginMutation();

  function onSubmit({ email, password }: FormValues) {
    login(
      {
        email,
        password,
      },
      {
        onSuccess: (data) => {
          if (data?.access ) { //&& data?.permissions?.length
            Cookies.set(AUTH_TOKEN, data.access);
            authorize(true);
            closeModal();
            return;
          }
          if (!data.access) {
            setErrorMessage(t('error-credential-wrong'));
          }
        },
        onError: (error: any) => {
          console.log(error.message);
          setErrorMessage(t('error-credential-wrong'));
           
        },
      }
    );
  }
  return (
    <LoginForm
      onSubmit={onSubmit}
      errorMessage={errorMessage}
      loading={loading}
    />
  );
};

export default Login;
