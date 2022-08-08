// https://tailwindcss.com/docs/dark-mode#supporting-system-preference-and-manual-selection

if (
  localStorage.theme === 'dark' ||
  (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  document.documentElement.classList.add('dark');
  localStorage.theme = 'dark';
} else {
  document.documentElement.classList.remove('dark');
  localStorage.removeItem('theme');
}
