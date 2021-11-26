import cn from 'classnames';
import { Waypoint } from 'react-waypoint';
import { Swiper, SwiperSlide, Navigation } from '@components/ui/slider';
import { Image } from '@components/ui/image';
import { Banner } from '@framework/types';
import { productPlaceholder } from '@lib/placeholders';
import Search from '@components/ui/search/search';
import { useAtom } from 'jotai';
import { displayHeaderSearchAtom } from '@store/display-header-search-atom';

interface BannerProps {
  banners: Banner[] | undefined;
  layout?: string;
}

const BannerWithSearch: React.FC<BannerProps> = ({ banners, layout }) => {
  const [_, setDisplayHeaderSearch] = useAtom(displayHeaderSearchAtom);

  const onWaypointPositionChange = ({
    currentPosition,
  }: Waypoint.CallbackArgs) => {
    if (!currentPosition || currentPosition === 'above') {
      setDisplayHeaderSearch(true);
    }
  };

  return (
    <div className="hidden lg:block relative">
      <div className="overflow-hidden -z-1">
        <div className="relative">
          <Swiper
            id="banner"
            loop={true}
            modules={[Navigation]}
            resizeObserver={true}
            allowTouchMove={false}
            slidesPerView={1}
          >
            {banners?.map((banner, idx) => (
              <SwiperSlide key={idx}>
                <div
                  className={cn('relative w-full h-screen', {
                    'max-h-140': layout === 'standard',
                  })}
                >
                  <Image
                    className="w-full h-full min-h-140"
                    src={banner.image?.original ?? productPlaceholder}
                    alt={banner.title ?? ''}
                    layout="fill"
                    objectFit="cover"
                  />
                  <div className="p-5 md:px-20 mt-8 absolute inset-0 w-full flex flex-col items-center justify-center text-center space-y-10">
                    <h1 className="text-4xl xl:text-5xl tracking-tight text-heading font-bold">
                      {banner?.title}
                    </h1>
                    <p className="text-base xl:text-lg text-heading">
                      {banner?.description}
                    </p>
                    <div className="max-w-3xl w-full">
                      <Search label="search" />
                    </div>
                    <Waypoint
                      onLeave={() => setDisplayHeaderSearch(true)}
                      onEnter={() => setDisplayHeaderSearch(false)}
                      onPositionChange={onWaypointPositionChange}
                    />
                  </div>
                </div>
              </SwiperSlide>
            ))}
          </Swiper>
        </div>
      </div>
    </div>
  );
};

export default BannerWithSearch;
