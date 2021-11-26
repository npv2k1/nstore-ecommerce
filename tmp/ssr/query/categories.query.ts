import {
  CategoriesQueryOptionsType,
  Category,
  QueryParamsType,
} from '@framework/types';
import { CoreApi } from './core-api';
import { API_ENDPOINTS } from '@framework/utils/endpoints';
import { useQuery } from 'react-query';

const CategoryService = new CoreApi(API_ENDPOINTS.PARENT_CATEGORIES);
export const fetchCategories = async ({ queryKey }: QueryParamsType) => {
  const params = queryKey[1];
  const {
    data: { data },
  } = await CategoryService.find(params as CategoriesQueryOptionsType);
  const tmp =  await CategoryService.find(params as CategoriesQueryOptionsType);
  // console.log("Categories tmp",{ categories: tmp.data });
  return { categories: tmp.data };
};
export const useCategoriesQuery = (options: CategoriesQueryOptionsType) => {
  return useQuery<{ categories: { data: Category[] } }, Error>(
    [API_ENDPOINTS.PARENT_CATEGORIES, options],
    fetchCategories
  );
};
