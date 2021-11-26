import { useUpdateCustomerMutation,useUpdateCustomerAddressMutation } from '@framework/customer/customer.query';
import {
  useModalAction,
  useModalState,
} from '@components/ui/modal/modal.context';
import AddressForm from '@components/address/address-form';
import { AddressType } from '@framework/utils/constants';
import { reload } from '@framework/utils/refresh-page';
import { useAtom } from 'jotai';

//
import {isUserUpdate} from "@store/user-atom"
type FormValues = {
  __typename?: string;
  title: string;
  type: AddressType;
  address: {
    country: string;
    city: string;
    state: string;
    zip: string;
    street_address: string;
  };
};

const CreateOrUpdateAddressForm = () => {
  const {
    data: { customerId, address },
  } = useModalState();
  const { closeModal } = useModalAction();
  
  const { mutate: updateProfile } = useUpdateCustomerAddressMutation();
  const [isUpdate, setIsUpdate] = useAtom(isUserUpdate)


  function onSubmit(values: FormValues) {
    const formattedInput = {
      title: values.title,
      type: values.type,
      address: {
        ...(address?.id && { id: address.id }),
        ...values.address,
      }
    };
    updateProfile(formattedInput);
    closeModal();
    setIsUpdate(true)
  }
  return <AddressForm onSubmit={onSubmit} />;
};

export default CreateOrUpdateAddressForm;
