import { ThemeSwitcher } from "./theme-switcher";

export default function FaceSwapHeader() {
  return (
    <header className="w-full bg-background border-b border-border p-4 flex justify-between items-center">
      <div className="flex items-center gap-2">
        <h1 className="text-2xl font-bold">Face Swap App</h1>
      </div>
      <ThemeSwitcher />
    </header>
  );
}
