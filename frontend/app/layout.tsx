import "./globals.css";

export const metadata = {
  title: "AI Packaging SaaS",
  description: "Generate packaging recommendations",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        style={{
          margin: 0,
          padding: 0,
          backgroundColor: "#0f0f0f",
          color: "#ffffff",
          fontFamily: "Arial, sans-serif",
        }}
      >
        {children}
      </body>
    </html>
  );
}
