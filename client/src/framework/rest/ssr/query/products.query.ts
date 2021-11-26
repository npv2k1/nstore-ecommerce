import {
  QueryParamsType,
  ProductsQueryOptionsType,
  Product,
} from '@framework/types';
import { CoreApi, ParamsType } from './core-api';
import { API_ENDPOINTS } from '@framework/utils/endpoints';
import {
  QueryKey,
  useInfiniteQuery,
  UseInfiniteQueryOptions,
  useQuery,
} from 'react-query';
const ProductService = new CoreApi(API_ENDPOINTS.PRODUCTS);

type PaginatedProduct = {
  data: Product[];
  paginatorInfo: any;
};
const fetchProducts = async ({
  queryKey,
  pageParam,
}: QueryParamsType): Promise<PaginatedProduct> => {
  const params = queryKey[1];
  let fetchedData: any = {};
  if (pageParam) {
    const response = await ProductService.fetchUrl(pageParam);
    fetchedData = response.data;
  } else {
    const response = await ProductService.find(params as ParamsType);
    fetchedData = response.data;
  }
  const { results, next } = fetchedData;
  // console.log(pageParam)
  // console.log("product data",{ data:results, paginatorInfo: mapPaginatorData({ ...next }) })

  return {
    data: results,
    paginatorInfo: {
      hasMorePages: next != null,
      nextPageUrl: next,
    },
  };
};

const useProductsQuery = (
  params: ProductsQueryOptionsType,
  options?: UseInfiniteQueryOptions<
    PaginatedProduct,
    Error,
    PaginatedProduct,
    PaginatedProduct,
    QueryKey
  >
) => {
  return useInfiniteQuery<PaginatedProduct, Error>(
    [API_ENDPOINTS.PRODUCTS, params],
    fetchProducts,
    {
      ...options,
      getNextPageParam: ({ paginatorInfo }) => paginatorInfo.nextPageUrl,
    }
  );
};

export { useProductsQuery, fetchProducts };

export const fetchProduct = async (slug: string) => {
  const { data } = await ProductService.findOne(slug);
  return data;
};

export const useProductQuery = (slug: string) => {
  return useQuery<Product, Error>([API_ENDPOINTS.PRODUCTS, slug], () =>
    fetchProduct(slug)
  );
};
