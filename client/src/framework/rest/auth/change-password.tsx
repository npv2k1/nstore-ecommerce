import { useChangePasswordMutation } from '@framework/auth/auth.query';
import { toast } from 'react-toastify';
import { useTranslation } from 'next-i18next';
import ChangePasswordForm from '@components/auth/change-password-form';
import { FormProvider, useForm } from 'react-hook-form';
import {
  changePasswordSchema,
  FormValues,
} from '@components/auth/change-password-validation-schema';
import { yupResolver } from '@hookform/resolvers/yup';

const ChangePassword = () => {
  const { t } = useTranslation('common');
  const methods = useForm({
    resolver: yupResolver(changePasswordSchema),
  });
  const { mutate: changePassword, isLoading: loading } =
    useChangePasswordMutation();

  function onSubmit({ newPassword, oldPassword }: FormValues) {
    changePassword(
      {
        old_password: oldPassword,
        new_password: newPassword,
      },
      {
        onSuccess: (data) => {
          if (!data.success) {
            methods.setError('oldPassword', {
              type: 'manual',
              message: data.message,
            });
            
          }
          toast.success(t('password-successful'));
          return;
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
          toast.error(t('Error'));
        },
      }
    );
  }
  return (
    <FormProvider {...methods}>
      <ChangePasswordForm loading={loading} onSubmit={onSubmit} />
    </FormProvider>
  );
};

export default ChangePassword;
