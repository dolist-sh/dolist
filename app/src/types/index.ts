export type Repo = {
  id: number;
  name: string;
  fullName: string;
  defaultBranch: string;
  language: string | null;
  url: string;
  provider: 'github';
  visibility: 'private' | 'public';
};

export type MonitoredRepo = {
  id: string;
  name: string;
  fullName: string;
  defaultBranch: string;
  userId: string;
  language: string | null;
  lastCommit: string | null;
  provider: 'github';
  visibility: 'private' | 'public';
  status: 'active' | 'inactive';
  parsedComments: ParsedComment[];
  createdAt: number;
  lastUpdated: number;
};

export type ParsedComment = {
  id: string;
  mrepoId: string;
  title: string;
  type: 'TODO';
  status: 'New' | 'Old' | 'Normal' | 'Resolved';
  commentStyle: 'oneline' | 'multiline';
  fullComment: string[];
  filePath: string;
  lineNumber: number;
  createdAt: number;
  lastUpdated: number;
};
