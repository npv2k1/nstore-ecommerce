import { useState } from 'react';
import Cookies from 'js-cookie';
import { FormProvider, useForm } from 'react-hook-form';
import { useLoginMutation, useRegisterMutation } from '@framework/auth/auth.query';
import { useTranslation } from 'next-i18next';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useModalAction } from '@components/ui/modal/modal.context';
import RegisterForm from '@components/auth/register-form';
import { useAtom } from 'jotai';
import { authorizationAtom } from '@store/authorization-atom';
import { AUTH_TOKEN } from '@lib/constants';

type FormValues = {
  username: string;
  email: string;
  password: string;
};

const registerFormSchema = yup.object().shape({
  username: yup.string().required('error-name-required'),
  email: yup
    .string()
    .email('error-email-format')
    .required('error-email-required'),
  password: yup.string().required('error-password-required'),
});

const Register = () => {
  const { t } = useTranslation('common');
  const [errorMessage, setErrorMessage] = useState('');
  const [_, authorize] = useAtom(authorizationAtom);
  const { closeModal } = useModalAction();

  const methods = useForm<FormValues>({
    resolver: yupResolver(registerFormSchema),
  });
  const { mutate: register, isLoading: loadingRegister } = useRegisterMutation();

  const { mutate: login, isLoading: loadingLogin } = useLoginMutation();
  function loginSubmit({ email, password }: FormValues) {
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

  function onSubmit({ username, email, password }: FormValues) {
    register(
      {
        username,
        email,
        password,
      },
      {
        onSuccess: (data) => {
          if (data?.id) {
            loginSubmit({ email, password });
            return;
          }
          if (!data?.id) {
            setErrorMessage(t('error-credential-wrong'));
          }
        },
        onError: (error) => {
          const {
            response: { data },
          }: any = error ?? {};
          Object.keys(data).forEach((field: any) => {
            methods.setError(field, {
              type: 'manual',
              message: data[field][0],
            });
          });
        },
      }
    );
  }
  return (
    <FormProvider {...methods}>
      <RegisterForm
        onSubmit={onSubmit}
        loading={loadingRegister}
        errorMessage={errorMessage}
      />
    </FormProvider>
  );
};

export default Register;
