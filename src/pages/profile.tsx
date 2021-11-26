import ProfileAddressGrid from '@components/profile/profile-address';
import Card from '@components/ui/cards/card';
import { useTranslation } from 'next-i18next';
import DashboardSidebar from '@components/dashboard/sidebar';
import { getLayout as getSiteLayout } from '@components/layouts/layout';
import ProfileInformation from '@framework/profile/profile-information';
import useUser from '@framework/auth/use-user';
import ProfileContact from '@components/profile/profile-contact';
import { isUserUpdate } from '@store/user-atom';
export { getStaticProps } from '@framework/ssr/common';
import { CoreApi } from '@framework/utils/core-api';
import { API_ENDPOINTS } from '@framework/utils/endpoints';
import {useState,useEffect} from "react"
import { useAtom } from 'jotai';

const CustomerService = new CoreApi(API_ENDPOINTS.CUSTOMER);
export const fetchMe = async () => {
  const { data } = await CustomerService.findAll();
  return { me: data };
};


const ProfilePage = () => {
  const { t } = useTranslation('common');
  const user = useUser()
  const [me, setMe] = useState(user.me)
  const [isUpdate, setIsUpdate] = useAtom(isUserUpdate)

  
  useEffect(()=>{
    // console.log("upppppp",isUpdate)
    async function updateUser() {
      let {me} = await fetchMe()
      console.log(me)
      setMe(me)    
    }
    setTimeout(()=>{
      if(isUpdate) updateUser() 
    }, 1000);    
    return ()=>{
      setIsUpdate(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[isUpdate])
 
  return (
    <div className="w-full overflow-hidden px-1 pb-1">
      <div className="mb-8">
        <ProfileInformation />
        <ProfileContact
          userId={me?.id!}
          profileId={me?.id!}
          contact={me?.phone!}
        />
      </div>

      <Card className="w-full">
        <ProfileAddressGrid
          userId={me?.id!}
          //@ts-ignore
          addresses={me?.address!}
          label={t('text-addresses')}
        />
      </Card>
    </div>
  );
};
const getLayout = (page: React.ReactElement) =>
  getSiteLayout(
    <div className="bg-gray-100 flex flex-col xl:flex-row items-start max-w-1920 w-full mx-auto py-10 px-5 xl:py-14 xl:px-8 2xl:px-14">
      <DashboardSidebar className="flex-shrink-0 hidden xl:block xl:w-80 me-8" />
      {page}
    </div>
  );

ProfilePage.authenticate = true;

ProfilePage.getLayout = getLayout;
export default ProfilePage;
