import { useGroupsQuery } from '@framework/groups/groups.query';
const useHomepage = () => {
  const { data } = useGroupsQuery();
  const homePage =
    data?.types?.find((type) => type?.settings?.isHome) ?? data?.types?.[0];
  return {
    homePage,
  };
};

export default useHomepage;
