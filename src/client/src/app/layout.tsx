import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { SidebarNav } from "@/components/sidebar-nav";
import { Separator } from "@/components/ui/separator";
import Link from "next/link";
import { Suspense } from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Simple Data Analytics",
  description: "A simple data analytics application for simple use case",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const navItems = [
    {
      title: "Upload File",
      href: "/upload",
    },
    {
      title: "Preview Data",
      href: "/preview",
    },
    {
      title: "Job Status",
      href: "/job-status",
    },
  ];
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen">
          <div className="flex flex-1 space-y-6 p-10">
            <div className="flex flex-1 flex-col ">
              <h2 className="text-2xl font-bold tracking-tight">
                <Link href="/">Simple Data Analytics</Link>
              </h2>
              <p className="text-gray-600">
                A simple data analytics application for simple use cases.
              </p>
              <Separator className="my-6" />
              <div className="flex flex-col flex-1 lg:flex-row lg:space-y-0">
                <aside className="-mx-4 mr-20">
                  <SidebarNav items={navItems} />
                </aside>
                <main className="flex-1">
                  {" "}
                  <Suspense fallback={<div>Loading...</div>}>
                    {children}
                  </Suspense>
                </main>
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
