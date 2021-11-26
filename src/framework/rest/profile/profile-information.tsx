import { useUpdateCustomerMutation } from '@framework/customer/customer.query';
import { toast } from 'react-toastify';
import { useTranslation } from 'next-i18next';
import ProfileForm from '@components/profile/profile-form';
import useUser from '@framework/auth/use-user';

const ProfileInformation = () => {
  const { t } = useTranslation('common');
  const { me } = useUser();
  const { mutate: updateProfile, isLoading: updating } =
    useUpdateCustomerMutation();

  function onSubmit(values: any) {
    if (!me) {
      return false;
    }
    updateProfile(
      {
        id: me.id,
        
        user: {
          id: me?.id,
          first_name: values.user.first_name,
          last_name: values.user.last_name,
        },
        bio: values.bio,
      },
      {
        onSuccess: () => {
          toast.success(t('profile-update-successful'));
          
        },
      }
    );
  }

  return <ProfileForm loading={updating} onSubmit={onSubmit} user={me} />;
};

export default ProfileInformation;
