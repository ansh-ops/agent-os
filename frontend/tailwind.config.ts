import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#f4f1ea",
        ink: "#122620",
        accent: "#17624a",
        panel: "#fffdf7",
        line: "#d8cfbe",
        warning: "#ab5d00",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "ui-sans-serif", "system-ui"],
        mono: ["var(--font-mono)", "ui-monospace", "SFMono-Regular"],
      },
      boxShadow: {
        panel: "0 14px 40px rgba(18, 38, 32, 0.08)",
      },
      backgroundImage: {
        grid: "linear-gradient(to right, rgba(23, 98, 74, 0.09) 1px, transparent 1px), linear-gradient(to bottom, rgba(23, 98, 74, 0.09) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};

export default config;
