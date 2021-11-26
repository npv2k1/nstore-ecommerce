import Button from '@components/ui/button';
import {
  useSendOtpCodeMutation,
  useVerifyOtpCodeMutation,
  useUpdateContactMutation
} from '@framework/auth/auth.query';
import { useState } from 'react';
import PhoneInput from 'react-phone-input-2';
import Alert from '@components/ui/alert';
import MobileOtpInput from 'react-otp-input';
import Label from '@components/ui/forms/label';
import { useTranslation } from 'next-i18next';
import 'react-phone-input-2/lib/bootstrap.css';

interface OTPProps {
  defaultValue: string | undefined;
  onVerify: (phoneNumber: string) => void;
}
export const PhoneForm: React.FC<OTPProps> = ({ defaultValue, onVerify }) => {
  const { t } = useTranslation('common');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [number, setNumber] = useState(defaultValue ?? '');
  const { mutate: updateContact, isLoading: loading } = useUpdateContactMutation();

  

  function onSendCodeSubmission() {
    updateContact(
      {
        phone: number,
      },
      {
        onSuccess: (data) => {
          if (data?.success) {
            
          }
          if (!data?.success) {
            console.log('text-otp-failed');
            setErrorMessage(data?.message);
          }
        },
        onError: (error: any) => {
          setErrorMessage(error?.response?.data?.message);
        },
      }
    );
  }
  return (
    <>
       
        <div className="flex items-center">
          <PhoneInput
            country={'us'}
            value={number}
            onChange={(phone) => setNumber(`+${phone}`)}
            inputClass="!p-0 !pe-4 !ps-14 !flex !items-center !w-full !appearance-none !transition !duration-300 !ease-in-out !text-heading !text-sm focus:!outline-none focus:!ring-0 !border !border-border-base !border-e-0 !rounded !rounded-e-none focus:!border-accent !h-12"
            dropdownClass="focus:!ring-0 !border !border-border-base !shadow-350"
          />
          <Button
            loading={loading}
            disabled={loading}
            onClick={()=>onVerify(number)}
            className="!rounded-s-none"
          >
            {/* {t('text-send-otp')} */}
            save
          </Button>
        </div>
      
        
      {errorMessage && (
        <Alert
          variant="error"
          message={t(errorMessage)}
          className="mt-4"
          closeable={true}
          onClose={() => setErrorMessage(null)}
        />
      )}
    </>
  );
};
