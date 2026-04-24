import { Layout } from "@/components/layout/Layout";
import { ReactNode } from "react";

interface PageHeaderProps {
  eyebrow: string;
  title: ReactNode;
  description?: string;
}

export const PageHeader = ({ eyebrow, title, description }: PageHeaderProps) => {
  return (
    <section className="container mx-auto px-6 lg:px-12 pt-16 pb-12">
      <div className="text-xs uppercase tracking-[0.3em] text-accent mb-4 animate-fade-in">
        {eyebrow}
      </div>
      <h1 className="font-display text-5xl lg:text-7xl text-foreground leading-[0.95] mb-6 animate-fade-in-up max-w-4xl">
        {title}
      </h1>
      {description && (
        <p className="text-lg text-muted-foreground max-w-2xl leading-relaxed animate-fade-in-up">
          {description}
        </p>
      )}
      <div className="suzani-divider mt-12 max-w-md" />
    </section>
  );
};

export const PageLayout = ({
  eyebrow,
  title,
  description,
  children,
}: PageHeaderProps & { children: ReactNode }) => {
  return (
    <Layout>
      <PageHeader eyebrow={eyebrow} title={title} description={description} />
      <section className="container mx-auto px-6 lg:px-12 pb-24">{children}</section>
    </Layout>
  );
};
