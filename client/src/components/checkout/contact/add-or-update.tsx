import { useModalAction, useModalState } from '@components/ui/modal/modal.context';
import { useUpdateContactMutation } from '@framework/auth/auth.query';
import { OTP} from '@framework/otp/otp';
import {PhoneForm} from '@framework/otp/phoneform';
import { reload } from '@framework/utils/refresh-page';
import { customerContactAtom } from '@store/checkout';
import { useAtom } from 'jotai';
import { useTranslation } from 'next-i18next';
import { toast } from 'react-toastify';

const AddOrUpdateCheckoutContact = () => {
  const { closeModal } = useModalAction();
  const { t } = useTranslation('common');
  const [contactNumber, setContactNumber] = useAtom(customerContactAtom);
  const { mutate: updateContact, isLoading: loading } = useUpdateContactMutation();

  function onContactUpdate(newPhoneNumber: string) {
    setContactNumber(newPhoneNumber);
    updateContact(
      {
        phone: newPhoneNumber,
      },
      {
        onSuccess:  () => {
          toast.success(t('profile-update-successful'));
          console.log('update contact success');
          // reload()
          closeModal();
        },
        onError:  (err) => {
          toast.error(t('error-something-wrong'));
          // reload()
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
      <PhoneForm defaultValue={contactNumber} onVerify={onContactUpdate} />
    </div>
  );
};

export default AddOrUpdateCheckoutContact;
