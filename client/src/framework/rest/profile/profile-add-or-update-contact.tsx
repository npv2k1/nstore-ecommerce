import {
  useModalAction,
  useModalState,
} from '@components/ui/modal/modal.context';
import { useUpdateContactMutation } from '@framework/auth/auth.query';
import { useUpdateCustomerMutation } from '@framework/customer/customer.query';
import { PhoneForm } from '@framework/otp/phoneform';
import { useTranslation } from 'next-i18next';
import { toast } from 'react-toastify';
import { useAtom } from 'jotai';


import { reload } from '@framework/utils/refresh-page'
import { isUserUpdate } from '@store/user-atom';

const ProfileAddOrUpdateContact = () => {
  const { t } = useTranslation('common');
  const {
    data: { customerId, contactNumber, profileId },
  } = useModalState();
  const { closeModal } = useModalAction();
  const { mutate: updateProfile } = useUpdateCustomerMutation();
  const { mutate: updateContact, isLoading: loading } = useUpdateContactMutation();
  const [isUpdate, setIsUpdate] = useAtom(isUserUpdate)


  function onContactUpdate(newPhoneNumber: string) {
    if (!customerId) {
      return false;
    }
    updateContact(
      {
        phone: newPhoneNumber,
      },
      {
        onSuccess:  () => {
          toast.success(t('profile-update-successful'));
          console.log('update contact success');
          setIsUpdate(true)
          closeModal();
        },
        onError:  (err) => {
          toast.error(t('error-something-wrong'));

          closeModal();
        },
      }
    ); 
  }
  return (
    <div className="p-5 sm:p-8 bg-light md:rounded-xl min-h-screen flex flex-col justify-center md:min-h-0">
      <h1 className="text-heading font-semibold text-sm text-center mb-5 sm:mb-6">
        {contactNumber ? t('text-update') : t('text-add-new')}{' '}
        {t('text-contact-number')}
      </h1>
      {/* <OTP defaultValue={contactNumber} onVerify={onContactUpdate} /> */}
      <PhoneForm defaultValue={contactNumber} onVerify={onContactUpdate} />
      
    </div>
  );
};

export default ProfileAddOrUpdateContact;
