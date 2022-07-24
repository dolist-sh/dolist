export type Repo = {
  id: number;
  name: string;
  defaultBranch: string;
  language: string;
  url: string;
  visibility: 'private' | 'public';
};
