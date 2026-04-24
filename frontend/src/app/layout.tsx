
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "./components/sidebar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Operational Resilience Command Center",
  description: "A centralized platform for managing and visualizing the resilience posture of critical IT services.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-gray-900 text-white`}>
        <div className="flex">
          <Sidebar />
          <main className="flex-grow p-6">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
