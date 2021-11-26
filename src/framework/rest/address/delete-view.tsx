import ConfirmationCard from '@components/ui/cards/confirmation';
import {
  useModalAction,
  useModalState,
} from '@components/ui/modal/modal.context';
import { useDeleteAddressMutation } from '@framework/address/address.query';
import { useAtom } from 'jotai';
import {isUserUpdate} from "@store/user-atom"
const AddressDeleteView = () => {
  const { data } = useModalState();
  const { closeModal } = useModalAction();
  const { mutate: deleteAddressById, isLoading } = useDeleteAddressMutation();
  const [isUpdate, setIsUpdate] = useAtom(isUserUpdate)
  function handleDelete() {
    deleteAddressById({ id: data?.addressId });
    setIsUpdate(true);
    closeModal();   

  }
  return (
    <ConfirmationCard
      onCancel={closeModal}
      onDelete={handleDelete}
      deleteBtnLoading={isLoading}
    />
  );
};

export default AddressDeleteView;
