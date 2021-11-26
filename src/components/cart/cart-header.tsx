import CartCheckBagIcon from '@components/icons/cart-check-bag';
import { formatString } from '@lib/format-string';
import usePrice from '@lib/use-price';
import { drawerAtom } from '@store/drawer-atom';
import { useCart } from '@store/quick-cart/cart.context';
import { useAtom } from 'jotai';
import { useTranslation } from 'next-i18next';

const CartHeader = () => {
  const { t } = useTranslation();
  const { totalUniqueItems, total } = useCart();
  const [_, setDisplayCart] = useAtom(drawerAtom);
  const { price: totalPrice } = usePrice({
    amount: total,
  });
  function handleCartSidebar() {
    setDisplayCart({ display: true, view: 'cart' });
  }
  return (
    <button
      className="product-cart flex flex-col items-center justify-center z-40 shadow-900 rounded text-light text-sm font-semibold transition-colors duration-200 focus:outline-none"
      onClick={handleCartSidebar}
    >
      <span className="flex pb-0.5 relative ">
        <CartCheckBagIcon className="flex-shrink-0 text-accent" width={30} height={34} />
        <span className="flex ms-2 absolute top-0 right-0 text-black bg-yellow-50 rounded-full font-bold text-center">
          {totalUniqueItems}
        </span>
      </span>
    </button>
  );
};

export default CartHeader;
