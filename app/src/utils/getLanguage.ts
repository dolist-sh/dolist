export type SUPPORTED_LANG = 'javascript' | 'python';

export function getLanguage(filePath: string): SUPPORTED_LANG | null {
  let result = null;

  const js = /(\.js$|\.ts$)/;
  const py = /(\.py$)/;

  js.test(filePath) ? (result = 'javascript') : null;
  py.test(filePath) ? (result = 'python') : null;

  return result;
}
