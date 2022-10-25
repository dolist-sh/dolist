import { useEffect, useState } from 'react';
import { ParsedComment, MonitoredRepo } from '../types';

export default function useCommentsPerType(mrepo: MonitoredRepo) {
  const [newComments, setNewComments] = useState<ParsedComment[]>([]);
  const [resolvedComments, setResolvedComments] = useState<ParsedComment[]>([]);
  const [oldComments, setOldComments] = useState<ParsedComment[]>([]);

  useEffect(() => {
    if (mrepo.parsedComments.length > 0) {
      setNewComments(mrepo.parsedComments.filter((e) => e.status == 'New'));
      setResolvedComments(mrepo.parsedComments.filter((e) => e.status == 'Resolved'));
      setOldComments(mrepo.parsedComments.filter((e) => e.status == 'Old'));
    }
  }, [mrepo]);

  return { newComments, resolvedComments, oldComments };
}
