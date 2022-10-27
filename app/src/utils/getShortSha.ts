export function getShortSha1(input: string, num = 7): string {
  return input.slice(0, num);
}
