import { fetchSettings } from './query/settings.query';
import { fetchGroups } from './query/groups.query';
import { API_ENDPOINTS } from '@framework/utils/endpoints';
import { GetStaticProps } from 'next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import { QueryClient } from 'react-query';
import { dehydrate } from 'react-query/hydration';

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const queryClient = new QueryClient();
  await queryClient.prefetchQuery(API_ENDPOINTS.SETTINGS, fetchSettings);
  await queryClient.prefetchQuery(API_ENDPOINTS.TYPE, fetchGroups);
  return {
    props: {
      ...(await serverSideTranslations(locale!, ['common'])),
      dehydratedState: JSON.parse(JSON.stringify(dehydrate(queryClient))),
    },
  };
};
