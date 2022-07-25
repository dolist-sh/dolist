export type Repo = {
  id: number;
  name: string;
  fullName: string;
  defaultBranch: string;
  language: string;
  url: string;
  visibility: 'private' | 'public';
};
