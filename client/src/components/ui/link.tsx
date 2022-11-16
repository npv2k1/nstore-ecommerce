import NextLink, { LinkProps as NextLinkProps } from 'next/link';

export interface LinkProps extends NextLinkProps {
  className?: string;
}

const Link: React.FC<LinkProps> = ({ href, children, className, ...props }) => {
  return (
    (<NextLink href={href} className={className} {...props}>

      {children}

    </NextLink>)
  );
};

export default Link;
