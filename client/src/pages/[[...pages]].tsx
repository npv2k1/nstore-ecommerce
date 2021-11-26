import { getLayout } from '@components/layouts/layout';
import Seo from '@components/seo/seo';
import useLayout from '@framework/utils/use-layout';
import { useWindowSize } from '@lib/use-window-size';
import dynamic from 'next/dynamic';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { scroller } from 'react-scroll';
export { getStaticPaths, getStaticProps } from '@framework/ssr/pages';
const Classic = dynamic(() => import('@components/layouts/classic'));
export default function Home() {
  const { query } = useRouter();
  const { width } = useWindowSize();
  const { layout, page } = useLayout();

  useEffect(() => {
    if (query.text || query.category) {
      scroller.scrollTo('grid', {
        smooth: true,
        offset: -110,
      });
    }
  }, [query.text, query.category]);
  let Component = Classic;
  return (
    <>
      <Seo title={page?.name!} url={page?.slug!} images={page?.banners!} />
      <Component />
    </>
  );
}

Home.getLayout = getLayout;
