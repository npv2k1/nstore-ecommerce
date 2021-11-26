import Coupon from '@framework/checkout/coupon';
import usePrice from '@lib/use-price';
import EmptyCartIcon from '@components/icons/empty-cart';
import { CloseIcon } from '@components/icons/close-icon';
import { useTranslation } from 'next-i18next';
import { useCart } from '@store/quick-cart/cart.context';
import {
  calculatePaidTotal,
  calculateTotal,
} from '@store/quick-cart/cart.utils';
import { useAtom } from 'jotai';
import {
  couponAtom,
  discountAtom,
  verifiedResponseAtom,
} from '@store/checkout';
import ItemCard from '@components/checkout/item/item-card';
import { ItemInfoRow } from '@components/checkout/item/item-info-row';
import PaymentGrid from '@components/checkout/payment/payment-grid';
import { PlaceOrderAction } from '@framework/checkout/place-order-action';

interface Props {
  className?: string;
}
const VerifiedItemList: React.FC<Props> = ({ className }) => {
  const { t } = useTranslation('common');
  const { items, isEmpty: isEmptyCart } = useCart();
  const [discount] = useAtom(discountAtom);

  const { price: shipping } = usePrice({
    amount: 1,
  });

  const base_amount = calculateTotal(items);
  console.log('base_amount', base_amount);

  const { price: sub_total } = usePrice({
    amount: base_amount,
  });

  const { price: total } = usePrice({
    amount: calculatePaidTotal(
      {
        totalAmount: base_amount,
        shipping_charge: 1,
      },
      Number(discount)
    ),
  });
  return (
    <div className={className}>
      <div className="flex flex-col border-b pb-2 border-border-200">
        {!isEmptyCart ? (
          items?.map((item) => {
            const notAvailable = false
            return (
              <ItemCard
                item={item}
                key={item.id}
                notAvailable={!!notAvailable}
              />
            );
          })
        ) : (
          <EmptyCartIcon />
        )}
      </div>

      <div className="space-y-2 mt-4">
        <ItemInfoRow title={t('text-sub-total')} value={sub_total} />
        <ItemInfoRow title={t('text-shipping')} value={shipping} />
        <div className="flex justify-between border-t-4 border-double border-border-200 pt-4">
          <p className="text-base font-semibold text-heading">
            {t('text-total')}
          </p>
          <span className="text-base font-semibold text-heading">{total}</span>
        </div>
      </div>
      <PaymentGrid className="bg-light p-5 border border-gray-200 mt-10" />
      <PlaceOrderAction>{t('text-place-order')}</PlaceOrderAction>
    </div>
  );
};

export default VerifiedItemList;
